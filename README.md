# Beam Anywhere Relay 

Requirements:

1. Python Django 2 (backend)
2. Firebase cloud messaging

# Running Beam Anywhere Relay on local machine (Windows)

## Backend:
- Install [Python 3.6 version](https://www.python.org/downloads/release/python-360/). Make sure that C:\Program Files (x86)\Python36-32; and C:\Program Files (x86)\Python36-32\Scripts; is part of your PATH.

- Install Redis

- Install vitrualenv to create individual environment
```
pip install virtualenv
```
- Create enviroment:
```
mkdir C:\virtualenv
cd C:\virtualenv
virtualenv bar
```
- Activate enviroment
```
C:\virtualenv\bar\Scripts\activate
```
- Clone repository
```
cd C:\
git clone https://github.com/BeamMW/beam-anywhere-relay.git
```
- Install requirements
```
cd beam-anywhere-relay
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

- Run server
```
python manage.py runserver
```

### Create api_key.json in root folder with api_key value from Firebase

# Beam Anywhere Relay API documentation 

### base URL: 
 https://bar.beam.mw/api

## 1. Link user.

### /link_user

### Method:

POST

### JSON row fields

| Field|Field type|Field description|
| ------------- |:-------------:| -----:|
| push_token | String | |
| username | String | |
| user_id | Number | |
| wallet_address | String | |
| msgr_type | String | |

### Example:
 https://bar.beam.mw/api/link_user

    {
        "push_token": "dxqpu9Zi8J4:APA91bFVMb-6C0lYk1n",
        "username": "username",
        "user_id": 1231435,
        "wallet_address": "8823a63ddf91b01c88d030e846",
        "msgr_type": "tg"
    }

## 2. Unlink user.

### /unlink_user

### Method:

DELETE

### JSON row fields

| Field|Field type|Field description|
| ------------- |:-------------:| -----:|
| username | String | |
| user_id | Number | |
| msgr_type | String | |

### Example:
https://bar.beam.mw/api/unlink_user

    {
        "user_id": 1231435,
        "msgr_type": "tg"
    }

## 3. Get linked user data.

### /get_user_data

### Method:

GET

### Request fields

| Field|Field type|Field description|
| ------------- |:-------------:| -----:|
| username | String | |
| user_id | Number | |
| msgr_type | String | |

### Example:
 
https://bar.beam.mw/api/get_user_data?username=somename&msgr_type=tg

## 4. Get linked users list.

### /linked_users_list

### Method:

GET

### Example:

https://bar.beam.mw/api/linked_users_list

### Response:

Array of user_id

## 5. Is user linked.

### /is_linked_user

### Method:

GET

### Request fields

| Field|Field type|Field description|
| ------------- |:-------------:| -----:|
| username | String | |
| user_id | Number | |
| msgr_type | String | |

### Example:

https://bar.beam.mw/api/is_linked_user?username=someusername&msgr_type=tg

## 6.Update notification.

### /update_notification

### Method:

PUT

### JSON row fields

| Field|Field type|Field description|
| ------------- |:-------------:| -----:|
| id | Number | Notification id |
| transaction_status | String | Default value = initiated |
| push_status | Number | in_progress=1, done=2, failed=3 |

### Example:
 https://bar.beam.mw/api/update_notification

    {
        "id": 11,
        "transaction_status": "sent"
    }

## 7. Send notification.

### /send_notification

### Method:

POST

### JSON row fields

| Field|Field type|Field description|
| ------------- |:-------------:| -----:|
| push_type | Number | Shout=1, Silent=0 |
| send_from | Number | User id |
| amount | Number | |
| fee | Number | |
| wallet_address | String | |
| msgr_type | String | |

### Example:
https://bar.beam.mw/api/send_notification

    {
        "push_type": 1,
        "send_from": 12312312,
        “amount”: 100,
        “fee”: 1,
        “msgr_type”: “tg”,
        “wallet_address”: “8823a63ddf91b01c88d030e846”
    }

## 8. Get notification data.

### /get_notification/<id>

### Method:

GET

### Example:
https://bar.beam.mw/api/get_notification/30

### Response:
    {
        "success": true,
        "data": {
            "id": 30,
            "transaction_status": "sent",
            "push_status": 2,
            "send_from": "43535434",
            "amount": 0,
            "fee": 10,
            "created_at": "2019-04-26T09:05:23.506348Z",
            "updated_at": "2019-04-26T09:05:31.596160Z",
            "push_type": 0
        }
    }
