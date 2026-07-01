from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.ask import router as ask_router
from backend.routes.impact import router as impact_router
from backend.routes.architecture import router as architecture_router
from backend.routes.clusters import router as clusters_router
from backend.routes.cluster_details import router as cluster_details_router
from backend.routes.component_impact import router as component_impact_router
from backend.routes.component_details import router as component_details_router
from backend.routes.architecture_graph import router as architecture_graph_router
from backend.routes.repository_stats import router as stats_router
from backend.routes.architecture_heatmap import router as architecture_heatmap_router
from backend.routes.analyze_repository import router as analyze_repository_router
from backend.routes.cluster_graph import router as cluster_graph_router
from backend.routes.cluster_details_graph import router as cluster_details_graph_router
from backend.routes.component_dependencies import router as dependency_router
from backend.routes.cluster_relationships import router as cluster_relationship_router
from backend.routes.layers import router as layers_router
from backend.routes import impact_heatmap
from backend.routes import smells
from backend.routes.circular_dependencies import router as circular_router
from backend.routes.architecture_health import router as health_router
from backend.routes.change_prediction import router as change_prediction_router
from backend.routes.blast_radius import router as blast_router
from backend.routes.layer_violations import router as layer_router
from backend.routes.layer_violations import router as layer_violations_router
from backend.routes.blast_radius import router as blast_router
from backend.routes.change_prediction import router as change_prediction_router
from backend.routes import critical_components
from backend.routes import refactoring_advisor



# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="Codebase Digital Twin API",
    version="1.0.0"
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================
# ROUTES
# ==========================================

app.include_router(ask_router)
app.include_router(impact_router)
app.include_router(architecture_router)
app.include_router(clusters_router)
app.include_router(cluster_details_router)
app.include_router(component_impact_router)
app.include_router(component_details_router)
app.include_router(architecture_graph_router)
app.include_router(stats_router)
app.include_router(architecture_heatmap_router)
app.include_router(analyze_repository_router)
app.include_router(cluster_graph_router)
app.include_router(cluster_details_graph_router)
app.include_router(dependency_router)
app.include_router(cluster_relationship_router)
app.include_router(layers_router)
app.include_router(impact_heatmap.router)
app.include_router(smells.router)
app.include_router(circular_router)
app.include_router(health_router)
app.include_router(change_prediction_router)
app.include_router(blast_router)
app.include_router(layer_router)
app.include_router(layer_violations_router)
app.include_router(blast_router)
app.include_router(change_prediction_router)
app.include_router(critical_components.router)
app.include_router(refactoring_advisor.router) 

# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Codebase Digital Twin Backend Running"
    }

# ==========================================
# DEBUG ROUTES
# ==========================================

@app.get("/routes")
def routes():
    return [
        {
            "path": route.path,
            "name": route.name
        }
        for route in app.routes
    ]