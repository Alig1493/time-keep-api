# Time Keeping API

* Api to allow authenticated users to clock in and clock out
* For now all the schedule endpoints are for authenticated users only

## Instructions:
* Run using makefile command `make up-build`
* Run tests using `make test`
* Create a superuser to use in admin panel using `make createsuperuser` and then following instructions
* After running successfully the server should be up on `http://0.0.0.0:8005` which will display the docs
* `http://0.0.0.0:8005/admin` should display the admin panel

## Apis:
* `http://0.0.0.0:8005/api/v1/token/`
  * Api for getting the login token. For now you can use the credentials you entered for the create superuser command
  * POST
  * Request payload: 
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  * Response payload: 
    ```json
    {
      "token": "string",
      "refresh": "string"
    }
    ```
* `http://0.0.0.0:8005/api/v1/refresh/`
  * Api for getting the login token. For now you can use the credentials you entered for the create superuser command
  * POST
  * Request payload: 
    ```json
    {
      "refresh": "string"
    }
    ```
  * Response payload: 
    ```json
    {
      "token": "string",
      "refresh": "string"
    }
    ```
* `http://0.0.0.0:8005/api/v1/schedules/`
  * Api for getting the login token. For now you can use the credentials you entered for the create superuser command
  * GET
  * Response payload: 
    ```json
    {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 6,
          "user": 4,
          "start_datetime": "2022-03-14T04:33:14.063469Z",
          "end_datetime": "2022-03-14T04:38:14.063469Z"
        }
      ]
    }
    ```
* `http://0.0.0.0:8005/api/v1/schedules/clock-in`
  * Api for getting the login token. For now you can use the credentials you entered for the create superuser command
  * POST
  * No Response for successful request, returns 200 only
  * Error Response 
  ```json ["Has unclocked entires for Daniel Nelson"]```

* `http://0.0.0.0:8005/api/v1/schedules/clock-out`
  * Api for getting the login token. For now you can use the credentials you entered for the create superuser command
  * POST
  * No Response for successful request, returns 200 only
  * Error Response 
  ```json ["Has no prior clock in times to clock out from for Daniel Nelson"]```

## Key Takeaways:
* For editing usernames I would add another endpoint under the authenticated user namespace to edit their names
  * For timesheet specific name editing another extra field in the database models to have optional name would suffice.
    * the name has to be unique to keep track of clock in/out times otherwise it will be hard to track and be utter chaos
  * In order to accommodate time sheet entry by public users I would setup a validation where I would request a username if the user is not logged in and if the user is logged in I would just use that username instead.
* For security I would add throttling to the clock-in/out apis for better security, because in the real world you;d rarely need to clock in/out so many times
* I have included database level constraints where 
  * the start time would be less than end time
  * the same user cannot have multiple identical start times as well as end times
* Validations considered so far:
  * if the user is clocking out even before clocking in
  * if the user is clocking in again before clocking out previously.
  * only allowed to clock out as long as a prior clockin time entry exists before.