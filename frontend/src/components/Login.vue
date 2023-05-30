<template>
  <div class="login-container">
    <div v-if="!create_acc" class="login-box">>
      <h2 class="login-title">Sign In</h2>
      <div class="form-group">
        <label for="signInUsername">Username</label>
        <input
          type="text"
          id="signInUsername"
          v-model="signInUsername"
          class="form-control"
          placeholder="Username"
          required autofocus
          :style="{ color: signInUsername === '' ? '#999999' : '' }"
        />
      </div>
      <div class="form-group">
        <label for="signInPassword">Password</label>
        <input
          type="password"
          id="signInPassword"
          v-model="signInPassword"
          class="form-control"
          placeholder="Password"
          required
          :style="{ color: signInPassword === '' ? '#999999' : '' }"
        />
      </div>
      <button class="btn btn-primary btn-block" @click="signIn">Sign In</button>
      <button class="btn btn-success btn-block" @click="createAccount">Create Account</button>
      <button class="btn btn-secondary btn-block" @click="backToMatches">Back To Matches</button>
    </div>
    <div v-else class="login-box">
      <h2 class="login-title">Create Account</h2>
      <div class="form-group">
        <label for="create-username">Username</label>
        <input
          type="text"
          id="create-username"
          v-model="createUsername"
          class="form-control"
          placeholder="Username"
          required
          :style="{ color: addUserForm.username === '' ? '#999999' : '' }"
        />
      </div>
      <div v-if="alertMessage" class="alert-message">{{ alertMessage }}</div>
      <div class="form-group">
        <label for="create-password">Password</label>
        <input
          type="password"
          id="create-password"
          v-model="createPassword"
          class="form-control"
          placeholder="Password"
          required
          :style="{ color: addUserForm.password === '' ? '#999999' : '' }"
        />
      </div>
      <button class="btn btn-primary btn-block" @click="submitAccount">Submit</button>
      <button class="btn btn-secondary btn-block" @click="createAccount">Back To Login</button>
    </div>
<!--    Para ver lo que vas haciendo en el forms-->
<!--    <div>-->
<!--    <button class="btn btn-normal" @click="showForms()">show details</button>-->
<!--      <b-card v-if="show" class="mt-3" header="Lo que has escrito:">-->
<!--        <pre class="m-0">{{ addUserForm }}</pre>-->
<!--      </b-card>-->
<!--     </div>-->
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

.alert-message {
  margin-top: 0;
  color: red;
  margin-bottom: 16px;
}
</style>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      logged: false,
      // Propiedades para el formulario de Sign In
      signInUsername: null,
      signInPassword: null,
      // Propiedades para el formulario de Create Account
      createUsername: null,
      createPassword: null,
      create_acc: false,
      token: null,
      addUserForm: {
        username: this.createUsername,
        password: this.createPassword
      },
      show: true,
      alertMessage: null
    }
  },
  methods: {
    signIn () {
      // Aquí puedes agregar la lógica para autenticar al usuario
      console.log('Sign In clicked')
    },
    createAccount () {
      this.create_acc = !this.create_acc
      // Aquí puedes agregar la lógica para crear una cuenta de usuario
      console.log('Create Account clicked')
    },
    backToMatches () {
      // Aquí puedes agregar la lógica para volver a la página de matches
      this.$router.push({ path: '/matches' })
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
    }, // 5.3
    initCreateForm () {
      this.creatingAccount = true
      this.addUserForm.username = null
      this.addUserForm.password = null
    },
    submitAccount () {
      this.addUserForm.username = this.createUsername
      this.addUserForm.password = this.createPassword
      console.log('Submit account clicked')
      const parameters = {
        username: this.createUsername,
        password: this.createPassword,
        available_money: 200.0,
        is_admin: 1,
        orders: []
      }
      this.postAccount(parameters)
    },
    postAccount (parameters) {
      console.log('Submit achieved')
      console.log(parameters)
      const path = 'http://localhost:8000/account'
      // Primero, realiza una solicitud GET al backend para verificar si el usuario ya existe
      // eslint-disable-next-line no-template-curly-in-string
      const pathget = 'http://localhost:8000/account/' + this.createUsername
      axios.get(pathget)
        .then(() => {
          // Si la solicitud GET tiene éxito, significa que el usuario ya existe
          // Muestra una alerta y no continúes con la creación de la cuenta
          this.alertMessage = 'El usuario ya existe'
        })
        .catch(() => {
        // Si la solicitud GET falla, significa que el usuario no existe
        // Puedes continuar con la creación de la cuenta enviando una solicitud POST
          axios.post(path, parameters)
            .then(() => {
              console.log('Account created')
              alert(JSON.stringify(this.addUserForm))
              console.log('arribo al reset')
              this.onReset()
              this.initCreateForm()
              console.log('arribo al push')
              this.createAccount()
            })
            .catch((error) => {
            // eslint-disable-next-line
            console.log(error)
            })
        })
    },
    onReset () {
      // Reset our form values
      this.createUsername = null
      this.createPassword = null
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    },
    getAccount () {
      // Realizar solicitud GET al backend para obtener la información de la cuenta del usuario
      // actualment no funciona
      const path = 'http://localhost:8000/account/' + this.createUsername
      // utilitzar de moment aquesthardcodejat
      // const path = 'http://localhost:8000/account/Oscar'
      const config = {
        headers: {
          Authorization: 'Bearer ' + this.token
        }
      }
      axios.get(path, config)
        .then((res) => {
          // Obtener el valor de is_admin del resultado de la respuesta
          this.is_admin = res.data.is_admin
        })
        .catch((error) => {
          console.error(error)
        })
    }
    // ,
    // showForms () {
    //   this.show = !this.show
    // }
  },
  created () {
  }
}
</script>
