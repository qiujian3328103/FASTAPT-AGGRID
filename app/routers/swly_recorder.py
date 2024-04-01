from fastapi import FastAPI, Request, Form, APIRouter, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from bokeh.plotting import figure
from bokeh.embed import components

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


# @router.get("/detail_page")
# async def detail_page(lot_id: str = Query(...), wafer_id: str = Query(...)):
#     # Process the selected row data
#     return {"lot_id": lot_id, "wafer_id": wafer_id}

@router.get("/detail_page", response_class=HTMLResponse)
async def detail_page(request: Request, lot_id: str = Query(...), wafer_id: str = Query(...)):
    print(lot_id, wafer_id)
    # Create a sample Bokeh plot
    # p = figure(plot_width=400, plot_height=400)
    # p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20)

    # Generate Bokeh components
    # script, div = components(p)
    # return templates.TemplateResponse("waferlabel.html", {"request": request, "lot_id": lot_id, "wafer_id": wafer_id, "plot_script": script, "plot_div": div})
    return templates.TemplateResponse("waferlabel.html", {"request": request, "lot_id": lot_id, "wafer_id": wafer_id})
