# gaia [![Build Status](https://travis-ci.com/lbarman/gaia.svg?branch=master)](https://travis-ci.com/lbarman/gaia) [![Coverage Status](https://coveralls.io/repos/github/lbarman/gaia/badge.svg?branch=master)](https://coveralls.io/github/lbarman/gaia?branch=master)



# Gotcha's:

`server` and `client` have their own pyenv, however the env for the server is a superset of the env for the client: everything can be build with the env of the server. The reason is so that the client doesn't have to download all the server packages. We don't care so much about the client packages in the server.