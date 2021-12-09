reticulate::source_python(system.file("python", "iol.py",
                                      package = "rapy", mustWork = TRUE))

# iol <- NULL
# .onLoad <- function(libname, pkgname) {
#   iol <<- reticulate::import_from_path("iol", system.file("python", "iol.py", package = "rapy", mustWork = TRUE))
# }

# df <- iol_scraping_panel_lider()
