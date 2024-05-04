from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Protocolos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numero_protocolo: int
    # status_protocolos: list["StatusProtocolo"] = Relationship(back_populates="protocolos")


class StatusProtocolo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numero_protocolo: int  # ToDo - join
    local_de_envio: str
    onde_esta: str
    motivo: str
    enviado_em: datetime
    total_dias_em_tramite: int

    # ToDo - Add relationships
    # protocolo_id: int = Field(foreign_key="protocolos.id")
    # protocolo: Protocolos = Relationship(back_populates="protocolos.status_protocolos")
