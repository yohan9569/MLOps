# -*- coding: utf-8 -*-

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from app.database import Base


class ModelCore(Base):
    __tablename__ = "model_core"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_name = Column(String, unique=True, nullable=False)
    model_file = Column(String, nullable=False)

    model_metadata_relation = relationship(
        "ModelMetadata", backref="model_core.model_name"
    )


class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    experiment_name = Column(String, unique=True, nullable=False)
    model_core_name = Column(
        String, ForeignKey("model_core.model_name"), nullable=False
    )
    experimenter = Column(String, nullable=False)
    version = Column(Float)
    train_mae = Column(Float, nullable=False)
    val_mae = Column(Float, nullable=False)
    train_mse = Column(Float, nullable=False)
    val_mse = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=now())
