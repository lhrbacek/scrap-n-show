# scrap-n-show
## Usage

Download the project and inside main folder execute `docker compose up`.

Then go to `localhost:8080` and see 500 offers (title and image) from sreality.cz, flats for sell.

Sometimes `flats_app` returns error ending with "Try again", so try again, usually it works.

Sometimes the server is up before the database which turns into error, please run `docker compose up` again.