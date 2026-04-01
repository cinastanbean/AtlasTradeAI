from __future__ import annotations

from dataclasses import dataclass

from .models import (
    AgentContext,
    AgentOutput,
    ExceptionMark,
    RiskAssessment,
    TaskDraft,
)


@dataclass(slots=True)
class RuleDecision:
    risk_level: str
    risk_type: str
    reason: str
    actions: list[str]
    tasks: list[TaskDraft]
    exceptions: list[ExceptionMark]


def evaluate_context(context: AgentContext) -> RuleDecision:
    event_type = context.trigger_event.event_type

    if event_type == "production.milestone_delayed":
        return _handle_production_delay(context)
    if event_type == "document.missing":
        return _handle_document_missing(context)
    if event_type == "logistics.delayed":
        return _handle_logistics_delay(context)
    if event_type == "payment.due_soon":
        return _handle_payment_due_soon(context)
    if event_type == "payment.overdue":
        return _handle_payment_overdue(context)

    return _handle_generic_followup(context)


def build_output(context: AgentContext, decision: RuleDecision) -> AgentOutput:
    summary = (
        f"订单 {context.order.order_no} 当前处于“{context.order.current_status}”阶段，"
        f"触发事件为 {context.trigger_event.event_type}。"
        f"{decision.reason}"
    )
    notification = (
        f"[{decision.risk_level.upper()}] 订单 {context.order.order_no} / "
        f"{context.customer.customer_name}：{decision.reason}。"
        f"建议优先处理：{decision.actions[0]}"
    )
    return AgentOutput(
        summary=summary,
        risk_assessment=RiskAssessment(
            level=decision.risk_level,
            risk_type=decision.risk_type,
            reason=decision.reason,
        ),
        recommended_actions=decision.actions,
        task_drafts=decision.tasks,
        exception_marks=decision.exceptions,
        notification_draft=notification,
    )


def _handle_production_delay(context: AgentContext) -> RuleDecision:
    customer_level = context.customer.customer_level
    risk_level = "high" if customer_level in {"战略客户", "重点客户"} else "medium"
    reason = "生产里程碑超时，订单存在交付延期风险"
    return RuleDecision(
        risk_level=risk_level,
        risk_type="delivery_delay",
        reason=reason,
        actions=[
            "联系工厂确认恢复时间并回填最新预计完成时间",
            "同步销售负责人评估是否需要提前告知客户",
            "检查是否需要调整发货计划或升级异常",
        ],
        tasks=[
            TaskDraft(
                title="确认工厂恢复时间",
                assignee_role="跟单员",
                priority="high",
                due_hint="2小时内",
            ),
            TaskDraft(
                title="同步销售确认客户沟通方案",
                assignee_role="销售",
                priority="medium",
                due_hint="今天内",
            ),
        ],
        exceptions=[
            ExceptionMark(
                exception_type="交付异常",
                exception_level="P1" if risk_level == "high" else "P2",
                reason=reason,
            )
        ],
    )


def _handle_document_missing(context: AgentContext) -> RuleDecision:
    reason = "单证资料不完整，可能阻塞发货或报关流程"
    return RuleDecision(
        risk_level="high",
        risk_type="document_blocking",
        reason=reason,
        actions=[
            "确认缺失单证清单并通知单证负责人补齐",
            "检查当前发货时间窗口是否受影响",
            "必要时升级为发货阻塞异常",
        ],
        tasks=[
            TaskDraft(
                title="补齐发货/报关单证",
                assignee_role="单证员",
                priority="high",
                due_hint="4小时内",
            )
        ],
        exceptions=[
            ExceptionMark(
                exception_type="单证异常",
                exception_level="P1",
                reason=reason,
            )
        ],
    )


def _handle_logistics_delay(context: AgentContext) -> RuleDecision:
    reason = "物流节点延迟，可能影响客户收货承诺"
    return RuleDecision(
        risk_level="medium",
        risk_type="logistics_delay",
        reason=reason,
        actions=[
            "联系物流服务商确认延误原因和最新时效",
            "评估是否需要同步客户新的预计到达时间",
            "关注是否引发后续对账或回款风险",
        ],
        tasks=[
            TaskDraft(
                title="确认物流延误原因",
                assignee_role="跟单员",
                priority="medium",
                due_hint="今天内",
            )
        ],
        exceptions=[
            ExceptionMark(
                exception_type="物流异常",
                exception_level="P2",
                reason=reason,
            )
        ],
    )


def _handle_payment_due_soon(context: AgentContext) -> RuleDecision:
    reason = "订单回款临近账期，建议提前安排客户付款确认"
    return RuleDecision(
        risk_level="medium",
        risk_type="payment_due",
        reason=reason,
        actions=[
            "联系客户确认付款计划和到账时间",
            "同步销售负责人确认沟通口径",
            "关注是否存在历史延迟付款记录",
        ],
        tasks=[
            TaskDraft(
                title="回款临期提醒",
                assignee_role="销售",
                priority="medium",
                due_hint="今天内",
            )
        ],
        exceptions=[],
    )


def _handle_payment_overdue(context: AgentContext) -> RuleDecision:
    days = context.payment.overdue_days
    reason = f"订单回款已逾期 {days} 天，存在资金回收风险"
    return RuleDecision(
        risk_level="high",
        risk_type="payment_overdue",
        reason=reason,
        actions=[
            "立即联系客户确认逾期原因与付款承诺",
            "同步财务和销售负责人评估后续催收动作",
            "如客户等级高且金额大，升级为重点回款异常",
        ],
        tasks=[
            TaskDraft(
                title="处理逾期回款",
                assignee_role="销售",
                priority="high",
                due_hint="2小时内",
            ),
            TaskDraft(
                title="复核逾期订单风险",
                assignee_role="财务",
                priority="high",
                due_hint="今天内",
            ),
        ],
        exceptions=[
            ExceptionMark(
                exception_type="回款异常",
                exception_level="P1",
                reason=reason,
            )
        ],
    )


def _handle_generic_followup(context: AgentContext) -> RuleDecision:
    reason = "订单发生关键状态变化，建议进行人工复核和后续推进"
    return RuleDecision(
        risk_level="low",
        risk_type="followup_required",
        reason=reason,
        actions=[
            "检查订单状态变化是否与计划一致",
            "确认是否需要补充任务或提醒",
            "记录本次事件的处理结果",
        ],
        tasks=[
            TaskDraft(
                title="复核订单状态变化",
                assignee_role="跟单员",
                priority="low",
                due_hint="今天内",
            )
        ],
        exceptions=[],
    )
