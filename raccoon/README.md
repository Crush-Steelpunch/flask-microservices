# Racoon

Users Info

`GET /`

List all of the data

`POST /<user_id>` DATA: `{ "token":"uuid","searchkey":"searchterm"}`

Search for a specific users data and User Info

`POST /addinfo/<user_id>` DATA: `{ "token":"uuid", "user_info_key":"keyname","user_info_value":"{json data}"}`
Add a specific users data and User Info

`DELETE /delinfo/<user_id>` DATA `{ "token":"uuid", "searchkey":"keyname"}`
Delete a specific users data and User Info

`DELETE /purgeinfo/<user_id>` DATA `{ "token":"uuid", 'yes-i-really-really-mean-it;:"purge-this-user-info-i-will-be-responsible-for-the-consequences"}`
Purge all user info