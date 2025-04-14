from datetime import datetime
from sqlalchemy import Column, Text, DateTime, UUID, ForeignKey, Boolean, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Packages(Base):
    __tablename__ = "packages"
    id = Column(UUID, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    version = Column(Text, nullable=False)
    description = Column(Text)
    repository = Column(Text)
    maintainer = Column(Text)
    build_config = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inputs = relationship("PackageInputs", back_populates="package", cascade="all, delete-orphan")
    dependencies = relationship("PackageDependencies", back_populates="package", cascade="all, delete-orphan")

class PackageInputs(Base):
    __tablename__ = "package_inputs"
    id = Column(UUID, primary_key=True, index=True)
    package_id = Column(UUID, ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    meta = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    package = relationship("Packages", back_populates="inputs")

class PackageDependencies(Base):
    __tablename__ = "package_dependencies"
    id = Column(UUID, primary_key=True, index=True)
    package_id = Column(UUID, ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    dependency_name = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    package = relationship("Packages", back_populates="dependencies")


