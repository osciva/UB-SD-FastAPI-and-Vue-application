<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">Sign In</h2>
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="username"
          class="form-control"
          placeholder="Username"
          required autofocus
          :style="{ color: username === '' ? '#999999' : '' }"
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-control"
          placeholder="Password"
          required
          :style="{ color: password === '' ? '#999999' : '' }"
        />
      </div>
      <button class="btn btn-primary btn-block" @click="signIn">Sign In</button>
      <button class="btn btn-success btn-block" @click="createAccount">Create Account</button>
      <button class="btn btn-secondary btn-block" @click="backToMatches">Back To Matches</button>
    </div>
  </div>
</template>

<style>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-box {
  width: 500px;
  height: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-control {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-block {
  width: 90%;
  margin: 10px auto 0;
}
</style>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      logged: false,
      username: null,
      password: null,
      token: null
    }
  },
  methods: {
    signIn () {
      // Aquí puedes agregar la lógica para autenticar al usuario
      console.log('Sign In clicked')
    },
    createAccount () {
      // Aquí puedes agregar la lógica para crear una cuenta de usuario
      console.log('Create Account clicked')
    },
    backToMatches () {
      // Aquí puedes agregar la lógica para volver a la página de matches
      console.log('Back To Matches clicked')
    },
    checkLogin () {
      const parameters = 'username=' + this.username + '&password=' + this.password
      const config = {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
      const path = 'http://localhost:8000/login'
      axios.post(path, parameters, config)
        .then((res) => {
          this.logged = true
          this.token = res.data.token
          this.$router.push({ path: '/', query: { logged: this.logged.toString(), username: this.username, token: this.token } })
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          alert('Username or Password incorrect')
        })
    }
  },
  created () {
    this.logged = this.$route.query.logged === 'true'
    this.username = this.$route.query.username
    this.token = this.$route.query.token
    if (this.logged === undefined) {
      this.logged = false
    }
  }
}
</script>
