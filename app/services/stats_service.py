from app.api.schema.stats import StatsResponse
from app.db.models.conversation import ConversationStatus
from app.db.repositories.unit_of_work import UnitOfWork


class StatsService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_stats(self) -> StatsResponse:

        total = self.uow.conversations.count()

        completed = self.uow.conversations.count_by_status(
            ConversationStatus.COMPLETED
        )

        failed = self.uow.conversations.count_by_status(
            ConversationStatus.FAILED
        )

        running = self.uow.conversations.count_by_status(
            ConversationStatus.RUNNING
        )

        avg_latency = self.uow.execution.average_latency()

        total_artifacts = self.uow.artifacts.count()

        total_messages = self.uow.messages.count()
        success_rate = (
            completed / total * 100
            if total
            else 0
        )

        avg_artifacts = (
            total_artifacts / total
            if total
            else 0
        )

        return StatsResponse(
            total_conversations=total,
            completed_conversations=completed,
            failed_conversations=failed,
            running_conversations=running,
            success_rate=round(success_rate, 2),
            average_latency_ms=round(avg_latency, 2),
            average_artifacts_per_conversation=round(avg_artifacts, 2),
            total_messages=total_messages,
        )