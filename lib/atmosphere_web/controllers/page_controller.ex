defmodule AtmosphereWeb.PageController do
  use AtmosphereWeb, :controller

  require Logger

  # %{
  #   "bme680" => %{
  #     "gas" => 62601,
  #     "humitidy" => 45.9937,
  #     "pressure" => 1007.58,
  #     "temperature" => 24.9142
  #   },
  #   "scd4x" => %{"co2" => 490, "relative_humidity" => 50.3052, "temperature" => 23.8587}
  # }

  @spec home(Plug.Conn.t(), any) :: Plug.Conn.t()
  def home(conn, _params) do
    # The home page is often custom made,
    # so skip the default app layout.
    render(conn, :home, layout: false)
  end

  def data(conn, params) do
    Logger.info(
      "Temperature bme=#{to_fahrenheit(params["bme680"]["temperature"])} scd4x=#{to_fahrenheit(params["scd4x"]["temperature"])}"
    )

    Logger.info("Gas #{params["bme680"]["gas"]}")

    Logger.info(
      "Humidity bme=#{params["bme680"]["humidity"]} scd4x=#{params["scd4x"]["relative_humidity"]}"
    )

    Logger.info("Pressure #{params["bme680"]["pressure"]}")
    Logger.info("CO2 #{params["scd4x"]["co2"]}")

    text(conn, "ok")
  end

  defp to_fahrenheit(celsius) do
    celsius * 9 / 5 + 32
  end
end
