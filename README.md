# flask-microservices

Suggested launch

```bash
git pull
docker compose build
docker compose up -d
docker exec bingo python3 createdb.py
docker exec lmnop python3 createdb.py
docker exec raccoon python3 createdb.py
export BINGOPORT=$(docker inspect bingo --format='{{(index (index .NetworkSettings.Ports "5000/tcp") 0).HostPort}}')
export LMNOPPORT=$(docker inspect lmnop --format='{{(index (index .NetworkSettings.Ports "5000/tcp") 0).HostPort}}')
export RACCOONPORT=$(docker inspect raccoon--format='{{(index (index .NetworkSettings.Ports "5000/tcp") 0).HostPort}}')
```

## Example Useage

### Bingo

```bash
curl localhost:$BINGOPORT
[{"id":3,"user_first_name":"Yuina","user_last_name":"Himoo","user_login_name":"YuinaH"},{"id":2,"user_first_name":"Mio","user_last_name":"Kisaragi","user_login_name":"MioK"},{"id":1,"user_first_name":"Shiori","user_last_name":"Fujisaki","user_login_name":"ShioriF"}]
```

```bash
curl localhost:$BINGOPORT/uid/1
[{"id":1,"user_first_name":"Shiori","user_last_name":"Fujisaki","user_login_name":"ShioriF"}]
```

```bash
curl -X POST -d '{ "fname":"wee","lname":"barry","login":"weeb"}'  -H "Content-Type: application/json" localhost:$BINGOPORT/adduser
```

### LMNOP

```bash
curl -X POST localhost:$LMNOPPORT/reqtoken/2
{"expired":"False","token":"2d26acfb-71a4-4931-bf2f-029ec1028f97"}
```

```bash
curl localhost:$LMNOPPORT/2d26acfb-71a4-4931-bf2f-029ec1028f97
{"expired":"False"}
```

### RACCOON

```bash
curl -X POST -d '{ "token":"2d26acfb-71a4-4931-bf2f-029ec1028f97","searchkey":"Physical_Data"}' -H "Content-Type: application/json" localhost:$RACCOONPORT/1
[{"user_id":1,"user_info_key":"Physical_Data","user_info_value":{"B":83,"Birthdate":"1978-05-27","Gender":"Female","H":84,"Height":158,"W":56,"bloodType":"A"}}]
```

```bash
curl -X POST -d '{ "token":"944bd02a-92b5-452d-8447-ffd32e053017", "user_info_key":"Barry_Info","user_info_value":{"thumb":[[false,"saved",-141244311.4902165,true,false,-733011461],false,"term",false,"move",true],"storm":1447655607.0926893,"wool":false,"pick":"room","proud":946847412.9938221,"went":-1934517076.1629238} }'  -H "Content-Type: application/json" localhost:$RACCOONPORT/addinfo/4
```

```bash
 curl -X POST -d '{ "token":"944bd02a-92b5-452d-8447-ffd32e053017","searchkey":"Barry_Info"}' -H "Content-Type: application/json" localhost:$RACCOONPORT/4
[{"user_id":4,"user_info_key":"Barry_Info","user_info_value":{"pick":"room","proud":946847412.9938221,"storm":1447655607.0926893,"thumb":[[false,"saved",-141244311.4902165,true,false,-733011461],false,"term",false,"move",true],"went":-1934517076.1629238,"wool":false}}]
```