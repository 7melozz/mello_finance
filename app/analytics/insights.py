from decimal import Decimal
from typing import Any


def generate_financial_insights(summary: dict[str, Any]) -> list[str]:
    insights: list[str] = []
    total_income = summary["total_income"]
    total_expenses = summary["total_expenses"]
    largest_category = summary.get("largest_expense_category")
    previous_expenses = summary.get("previous_month_expenses", None)

    if total_income > 0 and total_expenses / total_income >= Decimal("0.8"):
        insights.append("Você está gastando 80% ou mais da sua renda neste mês. Atenção ao orçamento.")

    if previous_expenses is not None and previous_expenses > Decimal("0"):
        change = ((total_expenses - previous_expenses) / previous_expenses) * Decimal("100")
        if change > 0:
            insights.append(f"Você gastou {change.quantize(Decimal('1.'))}% a mais que o mês anterior")
        elif change < 0:
            insights.append(f"Você gastou {abs(change).quantize(Decimal('1.'))}% a menos que o mês anterior")
        else:
            insights.append("Seu gasto ficou igual ao mês anterior")

    if largest_category:
        insights.append(f"Sua maior categoria de gasto foi {largest_category}")

    if not insights:
        insights.append("Seu comportamento financeiro está equilibrado neste mês")

    return insights
