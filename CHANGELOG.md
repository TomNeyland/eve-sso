### 0.1.0 (2015-05-15)


#### Bug Fixes

* **fixtures:** Fixes bug caused by spacing issues ([c2ff052d](https://github.com/TomNeyland/eve-sso/commit/c2ff052d))


#### Features

* **chat:** Adds initial chat features backed by socket.io ([84030bcf](https://github.com/TomNeyland/eve-sso/commit/84030bcf))
* **chatrooms:** Adds initial chatroom model. Adds FKs where they were missing on the group model ([f4e74a53](https://github.com/TomNeyland/eve-sso/commit/f4e74a53))
* **data:** populate command now inserts default data. Adds ChatroomData fixture. ([ddaed372](https://github.com/TomNeyland/eve-sso/commit/ddaed372))
* **gitter:** Adds webhook for gitter + travis builds ([847d941a](https://github.com/TomNeyland/eve-sso/commit/847d941a))
* **groups:** Adds initial models to support groups. converts models/ dir into models.py ([4fbf62d5](https://github.com/TomNeyland/eve-sso/commit/4fbf62d5))
* **manage:** Adds initial management commands. Includes commands for: runserver, shell, creat ([fe1bf517](https://github.com/TomNeyland/eve-sso/commit/fe1bf517))
* **models:** Adds initial character and crest auth models ([fb4e46ff](https://github.com/TomNeyland/eve-sso/commit/fb4e46ff))
* **oauth:**
  * Adds initial sso/oauth routes. Includes a send_static_file passthrough to make d ([ef1a05f3](https://github.com/TomNeyland/eve-sso/commit/ef1a05f3))
  * Adds initial oauth remote_app ([ac95c76b](https://github.com/TomNeyland/eve-sso/commit/ac95c76b))
* **readme:** Adds README.md ([636ac4cd](https://github.com/TomNeyland/eve-sso/commit/636ac4cd))