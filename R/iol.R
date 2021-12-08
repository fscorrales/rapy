reticulate::source_python(system.file("inst/python", "iol.py",
                                      package = "rapy", mustWork = TRUE))

df <- iol_scraping_panel_lider()
