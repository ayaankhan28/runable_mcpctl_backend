from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from models.packages_models import Packages, PackageInputs, PackageDependencies, PackageAliases
from database import get_db

router = APIRouter()

@router.get("/packages")
def get_packages(db: Session = Depends(get_db)):
    packages = db.query(Packages).all()
    return {"success": True, "data": packages}

@router.get("/packages/{package_id}")
def get_package_by_id(package_id: UUID, db: Session = Depends(get_db)):
    package = db.query(Packages).filter(Packages.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"success": True, "data": package}

@router.get("/packages/name/{package_name}")
def get_package_by_name(package_name: str, db: Session = Depends(get_db)):
    package = db.query(Packages).filter(Packages.name == package_name).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"success": True, "data": package}

@router.get("/packages/alias/{alias}")
def get_package_by_alias(alias: str, db: Session = Depends(get_db)):
    package_alias = db.query(PackageAliases).filter(PackageAliases.alias == alias).first()
    if not package_alias:
        raise HTTPException(status_code=404, detail="Package alias not found")
    return {"success": True, "data": package_alias.package}

@router.post("/packages")
def create_package(package_data: dict, db: Session = Depends(get_db)):
    try:
        # Create package
        package = Packages(
            name=package_data["name"],
            version=package_data["version"],
            description=package_data.get("description"),
            repository=package_data.get("repository"),
            maintainer=package_data.get("maintainer"),
            build_config=package_data["build_config"]
        )
        db.add(package)
        db.flush()

        # Add inputs
        if "inputs" in package_data:
            for input_data in package_data["inputs"]:
                package_input = PackageInputs(
                    package_id=package.id,
                    name=input_data["name"],
                    type=input_data["type"],
                    description=input_data.get("description"),
                    required=input_data["required"],
                    default_value=input_data.get("default_value")
                )
                db.add(package_input)

        # Add dependencies
        if "dependencies" in package_data:
            for dep_name in package_data["dependencies"]:
                dependency = PackageDependencies(
                    package_id=package.id,
                    dependency_name=dep_name
                )
                db.add(dependency)

        # Add aliases
        if "aliases" in package_data:
            for alias in package_data["aliases"]:
                package_alias = PackageAliases(
                    package_id=package.id,
                    alias=alias
                )
                db.add(package_alias)

        db.commit()
        return {"success": True, "data": package}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/packages/{package_id}")
def update_package(package_id: UUID, package_data: dict, db: Session = Depends(get_db)):
    package = db.query(Packages).filter(Packages.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    try:
        # Update package fields
        for key, value in package_data.items():
            if hasattr(package, key) and key not in ["id", "created_at", "updated_at"]:
                setattr(package, key, value)

        package.updated_at = datetime.utcnow()
        db.commit()
        return {"success": True, "data": package}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/packages/{package_id}")
def delete_package(package_id: UUID, db: Session = Depends(get_db)):
    package = db.query(Packages).filter(Packages.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    try:
        db.delete(package)
        db.commit()
        return {"success": True, "message": "Package deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))