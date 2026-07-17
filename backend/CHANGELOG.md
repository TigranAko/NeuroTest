# CHANGELOG

<!-- version list -->

## v0.5.0 (2026-07-17)

### Chores

- **env**: Add variavles for postgresql
  ([`79e8072`](https://github.com/TigranAko/NeuroTest/commit/79e807280d85ae701fba3c60c13b3c25e033a534))

- **uv**: Add alembic
  ([`b0c9f07`](https://github.com/TigranAko/NeuroTest/commit/b0c9f0791843a2157a1aa2328f76624f3ca549dd))

- **uv**: Add psycopg with binary and pool
  ([`2395b3a`](https://github.com/TigranAko/NeuroTest/commit/2395b3aab6dad818c4029e0029e41d5ec3f74433))

- **uv**: Add psycopg3
  ([`026a266`](https://github.com/TigranAko/NeuroTest/commit/026a266ebf70cca8ef07c085b9dc9a432a1b6851))

- **uv**: Add sqlalchemy[asyncio]
  ([`e7cc53b`](https://github.com/TigranAko/NeuroTest/commit/e7cc53b8791216e6bd78cadba32dba95bac789fb))

### Documentation

- Add alembic files and user model to readme
  ([`73cbfe7`](https://github.com/TigranAko/NeuroTest/commit/73cbfe7f8a6f9b77a5e4ab1571f14750ede15b77))

- Add database technologies to readme
  ([`655c57d`](https://github.com/TigranAko/NeuroTest/commit/655c57de080ecea0f5351bff89ad06466e76d17c))

- Change endpoint /myid to /me, get user info
  ([`7b63304`](https://github.com/TigranAko/NeuroTest/commit/7b6330428423d43829fb48ebc72273d26ff338df))

- Change run services in readme
  ([`542969e`](https://github.com/TigranAko/NeuroTest/commit/542969e9fd7010b269c9d48c4783da955ef37e8a))

### Features

- **alembic**: Add metadata for autogenerate migrations
  ([`012f4ac`](https://github.com/TigranAko/NeuroTest/commit/012f4ac018a161bd4ba89f37008ecce99706a315))

- **alembic**: Add timestamp for table users
  ([`012571b`](https://github.com/TigranAko/NeuroTest/commit/012571b9b03358382e7b57df8ca020e57992e3b4))

- **alembic**: Add user table
  ([`6078130`](https://github.com/TigranAko/NeuroTest/commit/607813072aa944f6def7832e229448c81649052c))

- **alembic**: Init alembic
  ([`149db45`](https://github.com/TigranAko/NeuroTest/commit/149db4575160d82e04e4a97d094c8acac9f96176))

- **api**: Add timestamp for schemas
  ([`67d77be`](https://github.com/TigranAko/NeuroTest/commit/67d77be567d2739884aa0e8e6bb395134e7c57f5))

- **db**: Add async database
  ([`31c5991`](https://github.com/TigranAko/NeuroTest/commit/31c59916892fb4199909f34bbdaa2e0f66ec8453))

- **db**: Add user model
  ([`5a97857`](https://github.com/TigranAko/NeuroTest/commit/5a978577b33e85656c210f169c4bbd88a677581f))

- **db**: Create tables in lifespan
  ([`9be35d1`](https://github.com/TigranAko/NeuroTest/commit/9be35d12f685dd8ea7f559649597bff3f503fb5a))

- **docker**: Add adminer to compose
  ([`ae275d2`](https://github.com/TigranAko/NeuroTest/commit/ae275d2ee95eb5ee67a7e77d73e02ed5e07a7a6e))

- **docker**: Add docker-compose with fastapi
  ([`274ab43`](https://github.com/TigranAko/NeuroTest/commit/274ab433d00de0c7761d71b46c78a43300400810))

- **docker**: Add entrypoint for alembic upgrade head
  ([`cf1c714`](https://github.com/TigranAko/NeuroTest/commit/cf1c7147140b61ae6a30299caf90f65df1b06d26))

- **docker**: Add postgres to compose
  ([`770ec9d`](https://github.com/TigranAko/NeuroTest/commit/770ec9ddf9289ed95867f08d31ec2fc1840213cc))

- **env**: Add settings for postgres
  ([`1af3f3a`](https://github.com/TigranAko/NeuroTest/commit/1af3f3acfaee341a28fd260b0b1a9ab5ae7dadc5))

- **models**: Add timestamp mixin
  ([`8c6ef59`](https://github.com/TigranAko/NeuroTest/commit/8c6ef5947a956a6fb215f9412053b2576d797701))

- **user**: Add add_one() to UserRepository
  ([`4358b85`](https://github.com/TigranAko/NeuroTest/commit/4358b85e2e72c0bf332c0fa2160f6ad8a0e0aa58))

- **user**: Add get_by_username in repository
  ([`9c9ab21`](https://github.com/TigranAko/NeuroTest/commit/9c9ab21559505b5cc7cdc7c59a513149a3924c82))

- **user**: Change information about current user on endpoint auth/me
  ([`4af69fc`](https://github.com/TigranAko/NeuroTest/commit/4af69fc06ec57083ce70db942c2d125099775311))

- **user**: Use repository for login
  ([`d52fee7`](https://github.com/TigranAko/NeuroTest/commit/d52fee7caa764e6280644b3be1c85ac3eb5371c1))

- **user**: Use repository for register
  ([`9994484`](https://github.com/TigranAko/NeuroTest/commit/9994484988a29b92ff7bd67849213c0132239555))

- **user**: Verify user's existence durning registration
  ([`7cdc52d`](https://github.com/TigranAko/NeuroTest/commit/7cdc52dd8c0f67be02078c418b605e2f8dcdd2cb))


## v0.4.0 (2026-07-14)

### Bug Fixes

- **auth**: Add exception user not found and fix some problems
  ([`cccc878`](https://github.com/TigranAko/NeuroTest/commit/cccc878a2dd0cdcc52ea654508849825e7510186))

- **auth**: Set refresh timeout
  ([`614a69d`](https://github.com/TigranAko/NeuroTest/commit/614a69d6cf73851bd4e8209cb1458b737f24789e))

### Chores

- **uv**: Add argon2-cffi
  ([`e62fbea`](https://github.com/TigranAko/NeuroTest/commit/e62fbead95c33e8d06967e3287145fb6e7fa7f2c))

- **uv**: Add pyjwt to pyproject and uv.lock
  ([`544511c`](https://github.com/TigranAko/NeuroTest/commit/544511c0dc3dfe6ca5244f33be7a1c26789b341d))

- **uv**: Update uv.lock to 0.3.0
  ([`138cdb9`](https://github.com/TigranAko/NeuroTest/commit/138cdb9e415ea2ca8e2f11b971fc547ed8ec0fb7))

### Documentation

- Add auth endpoints to readme
  ([`616c547`](https://github.com/TigranAko/NeuroTest/commit/616c547c76a6b4de669a533ab0b6d6f10fda18f9))

- Add auth files to readme
  ([`d65e378`](https://github.com/TigranAko/NeuroTest/commit/d65e37898ef5b7ea0485945885d1a32bd525b0fd))

- Add auth technologies to readme
  ([`3cbc390`](https://github.com/TigranAko/NeuroTest/commit/3cbc3906af200528d364da3b99325a4ae234e26e))

- Change environment information in readme
  ([`da107f1`](https://github.com/TigranAko/NeuroTest/commit/da107f1790c66b9c10ad660e05c8a7ddb1c9e662))

### Features

- **api**: Add authorization to router llm (neurotest)
  ([`fe219f8`](https://github.com/TigranAko/NeuroTest/commit/fe219f82a71e94c48465fa5aaa40e5564b0a0ba1))

- **auth**: Add authorize button to swagger by OAuth2PasswordBearer
  ([`e02d461`](https://github.com/TigranAko/NeuroTest/commit/e02d4613ef92086918da68663eac3f51c5382526))

- **auth**: Add basic regestration with fake db
  ([`d346824`](https://github.com/TigranAko/NeuroTest/commit/d3468247756a4cbe1c990a1cbda645984367f614))

- **auth**: Add dependency for extracting user_id from access token
  ([`8950cc0`](https://github.com/TigranAko/NeuroTest/commit/8950cc0d9865f402e44c78a964ced2511b3a20b4))

- **auth**: Add jwt service for create tokens
  ([`a1e8e6d`](https://github.com/TigranAko/NeuroTest/commit/a1e8e6d9bedbb998fe3a145ec62f3fc0846f57bd))

- **auth**: Add login endpoint with jwt and cookie
  ([`7d31f03`](https://github.com/TigranAko/NeuroTest/commit/7d31f031d526ed34ae6742c928859c4ce9e14116))

- **auth**: Add logout endpoint with delete refresh cookie
  ([`1c4a3ba`](https://github.com/TigranAko/NeuroTest/commit/1c4a3ba3898826bbf1bb1c9141af6a678bb91691))

- **auth**: Add password hasher with argon2
  ([`1e00b31`](https://github.com/TigranAko/NeuroTest/commit/1e00b3183862529f9c1d175d01dff12017be3d29))

- **auth**: Add token refresh endpoint
  ([`5e62860`](https://github.com/TigranAko/NeuroTest/commit/5e628607818d073cb28a5d0a294b6788fb6b540b))

- **env**: Add environment variables for auth
  ([`ecfd379`](https://github.com/TigranAko/NeuroTest/commit/ecfd379f453488cc103f0d26443d98c8221f7cc3))

- **env**: Add settings forauth
  ([`dba468e`](https://github.com/TigranAko/NeuroTest/commit/dba468e32923d4672aa686605df771fd2c74d952))


## v0.3.0 (2026-07-06)

### Chores

- **ruff**: Sort imports questions and answers
  ([`b1381c1`](https://github.com/TigranAko/NeuroTest/commit/b1381c1eac17207318e6b551d1e31d8dbf7b2b7e))

- **uv**: Update uv.lock version
  ([`36b3327`](https://github.com/TigranAko/NeuroTest/commit/36b3327bbfedc571aa6cde20a18adeaf79254678))

### Continuous Integration

- Remove semantic release on PR
  ([`83a8c36`](https://github.com/TigranAko/NeuroTest/commit/83a8c36a3e8ac35da829efc6ed89d8be421bc02b))

- Update actions/checkout from v4 to v6
  ([`d4c7ea3`](https://github.com/TigranAko/NeuroTest/commit/d4c7ea3cf6abd1a81c87c3749a829302c01dda30))

### Documentation

- Remove todos from readme
  ([`473fc4b`](https://github.com/TigranAko/NeuroTest/commit/473fc4b513523623edc4d7775aa6a39400e83a81))

- Update description in README.md
  ([`1fce6d2`](https://github.com/TigranAko/NeuroTest/commit/1fce6d2dc2a9943675db92f9445924de52be3135))

- Update project architecture, add files for tests, questions, answers
  ([`0ec74e4`](https://github.com/TigranAko/NeuroTest/commit/0ec74e4718866576f655612bda22a52f31d7d50b))

- **api**: Add endpoints for test, question, answer objects
  ([`e554b4d`](https://github.com/TigranAko/NeuroTest/commit/e554b4d7b2acd9bd77ed886c7bb98e00cc53e9e2))

### Features

- **api**: Add AnswerService with basic crud
  ([`e7a0fc0`](https://github.com/TigranAko/NeuroTest/commit/e7a0fc06dede692800678a5e23915f4735b20f02))

- **api**: Add FileAnswerRepository with basic crud
  ([`063b436`](https://github.com/TigranAko/NeuroTest/commit/063b43680d8470ceeed127fc56ce96f32b0866c3))

- **api**: Add FileQuestionRepository with basic crud
  ([`53c27f3`](https://github.com/TigranAko/NeuroTest/commit/53c27f3a0c6b03f278516b9b6c19328183415fe3))

- **api**: Add FileStorage for file management
  ([`b1a4171`](https://github.com/TigranAko/NeuroTest/commit/b1a417142bd2b88927840f06493ed93880c40ea8))

- **api**: Add FileTestRepository
  ([`94ff405`](https://github.com/TigranAko/NeuroTest/commit/94ff40552c0091683dd34d3467c499ba933ce3bc))

- **api**: Add handlers for Answer object crud
  ([`5b1140a`](https://github.com/TigranAko/NeuroTest/commit/5b1140acc3de682ac1459ff1a2361995b46c2924))

- **api**: Add handlers for Question object crud
  ([`e1d5a81`](https://github.com/TigranAko/NeuroTest/commit/e1d5a8189cf1267e0f111286b1c671e44337291d))

- **api**: Add handlers for Test object
  ([`a44d720`](https://github.com/TigranAko/NeuroTest/commit/a44d720570a6a0f264994e764a22c3c889028cff))

- **api**: Add interface for AnswerRepository with basic crud
  ([`f327b8d`](https://github.com/TigranAko/NeuroTest/commit/f327b8d9a8dc0189c6bbd60b3ec008ba34c494b3))

- **api**: Add interface for QuestionRepository with basic crud
  ([`3251bf0`](https://github.com/TigranAko/NeuroTest/commit/3251bf0ebf2a3831e06e9ef8c267b7a7309a2b21))

- **api**: Add interface for test repository
  ([`7668411`](https://github.com/TigranAko/NeuroTest/commit/7668411e19c5cbc14af1f6f05219f9f3007627a0))

- **api**: Add QuestionService with basic crud
  ([`33153f5`](https://github.com/TigranAko/NeuroTest/commit/33153f5198bb4fcbd983631b244f7f16ebf83701))

- **api**: Add TestService
  ([`2794f52`](https://github.com/TigranAko/NeuroTest/commit/2794f527bb3d976627309a603e0427b44a016d2d))


## v0.2.0 (2026-06-29)

### Features

- **test,ci**: Test update minor version
  ([`f88bb86`](https://github.com/TigranAko/NeuroTest/commit/f88bb860c5d2f3aa5df5405f92524795dd1e49ba))


## v0.1.0 (2026-06-29)

- Initial Release

## v1.0.1 (2026-06-28)

### Bug Fixes

- **ci**: Update pyproject.toml, add 2 parameters and version variables
  ([`35359b0`](https://github.com/TigranAko/NeuroTest/commit/35359b016baa00385940bef83ed0030d71f97897))


## v1.0.0 (2026-06-28)

- Initial Release
