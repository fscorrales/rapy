# Generate R6 Class
IOLConnection <- R6::R6Class(
  classname = "IOLConnection",
  private = list(
    response = NULL,
    user = NULL,
    password = NULL
  ),
  # active = list(
  #   tables = function(value) {
  #     if (missing(value)) {
  #       private$.tables
  #     } else {
  #       stop("`$tables` is read only", call. = FALSE)
  #     }
  #   },
  #   fields = function(value) {
  #     if (missing(value)) {
  #       private$.fields
  #     } else {
  #       stop("`$fields` is read only", call. = FALSE)
  #     }
  #   }
  # ),
  public = list(
    data = NULL,
    initialize = function(user = NULL, password = NULL) {

      stopifnot(is.character(user), length(user) == 1)
      stopifnot(is.character(password), length(password) == 1)

      private$user = user
      private$password = password
      self$autenticar()

    },
    autenticar = function() {

      private$response = iol_authentication(private$user, private$password)
      invisible(self)

    },
    expired_token = function() {

      sec_to_expire = iol_seconds_to_expire(private$response)

      if(sec_to_expire < 10) {
        message("Getting new Token")
        private$response = iol_authentication(private$user, private$password)
      }

    },
    estado_de_cuenta = function(...) {

      self$expired_token()
      df = iol_get_estado_de_cuenta(private$response)
      self$data = dplyr::as_tibble(df)
      self$data

    },
    finalize = function() {

      #Message
      message("Disconnecting and cleaning database.")
      #Cleaning data
      private$response = NULL
      private$user = NULL
      private$password = NULL

    }
  )
)
