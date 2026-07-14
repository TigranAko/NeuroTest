# CHANGELOG

<!-- version list -->

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
