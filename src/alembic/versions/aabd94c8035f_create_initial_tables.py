from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "aabd94c8035f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "salas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.Column("unidade", sa.Integer(), nullable=False),
        sa.Column("bloco", sa.Integer(), nullable=False),
        sa.Column("potencial_base_kw", sa.Float(), nullable=False, server_default="2.5"),
        sa.Column("setpoint_atual", sa.Float(), nullable=False, server_default="24.0"),
        sa.Column("ativa", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dispositivos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sala_id", sa.Integer(), nullable=False),
        sa.Column("mac_address", sa.String(), nullable=True),
        sa.Column("modelo_chip", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="offline"),
        sa.Column("last_seen", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["sala_id"], ["salas.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "telemetrias",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sala_id", sa.Integer(), nullable=False),
        sa.Column("dispositivo_id", sa.Integer(), nullable=False),
        sa.Column("co2", sa.Float(), nullable=False),
        sa.Column("temperatura", sa.Float(), nullable=False),
        sa.Column("umidade", sa.Float(), nullable=True),
        sa.Column("corrente_rms", sa.Float(), nullable=False),
        sa.Column("potencia_ativa_kw", sa.Float(), nullable=False),
        sa.Column("setpoint", sa.Float(), nullable=False),
        sa.Column("economia_ciclo_brl", sa.Float(), nullable=True),
        sa.Column("economia_acumulada_brl", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("update_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["dispositivo_id"], ["dispositivos.id"]),
        sa.ForeignKeyConstraint(["sala_id"], ["salas.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "comandos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sala_id", sa.Integer(), nullable=False),
        sa.Column("acao", sa.String(), nullable=False),
        sa.Column("setpoint_alvo", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["sala_id"], ["salas.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("comandos")
    op.drop_table("telemetrias")
    op.drop_table("dispositivos")
    op.drop_table("salas")
