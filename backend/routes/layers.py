from fastapi import APIRouter
import pickle
import os

router = APIRouter()


# ==========================================
# LOAD ARCHITECTURE SUMMARIES
# ==========================================

def load_summaries():

    path = "data/architecture_summaries.pkl"

    if not os.path.exists(path):
        return []

    with open(path, "rb") as f:
        return pickle.load(f)


# ==========================================
# DETECT LAYER
# ==========================================

def detect_layer(component_name, file_path=""):

    name = component_name.lower()
    path = file_path.lower()

    # =====================================
    # API Layer
    # =====================================

    if any(keyword in path for keyword in [
        "routing",
        "route",
        "router",
        "endpoint",
        "api",
        "websocket"
    ]):
        return "API Layer"

    if any(keyword in name for keyword in [
        "router",
        "route",
        "endpoint",
        "api",
        "view",
        "apirouter"
    ]):
        return "API Layer"

    # =====================================
    # Service Layer
    # =====================================

    if any(keyword in path for keyword in [
        "dependencies",
        "dependency",
        "service",
        "manager",
        "handler",
        "middleware"
    ]):
        return "Service Layer"

    if any(keyword in name for keyword in [
        "service",
        "manager",
        "handler",
        "middleware",
        "dependency"
    ]):
        return "Service Layer"

    # =====================================
    # Data Layer
    # =====================================

    if any(keyword in path for keyword in [
        "repository",
        "database",
        "dao",
        "query",
        "storage"
    ]):
        return "Data Layer"

    if any(keyword in name for keyword in [
        "repository",
        "dao",
        "query",
        "database"
    ]):
        return "Data Layer"

    # =====================================
    # Domain Layer
    # =====================================

    if any(keyword in path for keyword in [
        "model",
        "models",
        "schema",
        "schemas",
        "entity",
        "params",
        "responses"
    ]):
        return "Domain Layer"

    if any(keyword in name for keyword in [
        "model",
        "schema",
        "entity",
        "response"
    ]):
        return "Domain Layer"

    # =====================================
    # Infrastructure Layer
    # =====================================

    if any(keyword in path for keyword in [
        "utils",
        "util",
        "helper",
        "helpers",
        "common",
        "config",
        "logging"
    ]):
        return "Infrastructure Layer"

    if any(keyword in name for keyword in [
        "util",
        "helper",
        "config",
        "logger"
    ]):
        return "Infrastructure Layer"

    # =====================================
    # Default
    # =====================================

    return "Business Layer"


# ==========================================
# GET LAYERS
# ==========================================

@router.get("/layers")
def get_layers():

    summaries = load_summaries()

    layers = {}

    for component in summaries:

        name = component.get("name", "unknown")
        file_path = component.get("file", "")

        layer = detect_layer(name, file_path)

        if layer not in layers:
            layers[layer] = []

        layers[layer].append({
            "name": name,
            "file": file_path
        })

    response = []

    for layer_name, components in layers.items():

        response.append({
            "layer": layer_name,
            "size": len(components),
            "components": components
        })

    response.sort(
        key=lambda x: x["size"],
        reverse=True
    )

    return {
        "success": True,
        "layers": response
    }