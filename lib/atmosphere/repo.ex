defmodule Atmosphere.Repo do
  use Ecto.Repo,
    otp_app: :atmosphere,
    adapter: Ecto.Adapters.Postgres
end
