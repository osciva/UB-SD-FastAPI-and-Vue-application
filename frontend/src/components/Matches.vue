<template>
  <div id="app" class="vh-100">
<!--    <button class="btn btn-success btn-lg" @click="buyTicket" :disabled="money_available < price_match"> Buy ticket </button>-->
<!--    <button class="btn btn-danger btn-lg" @click="returnTicket" :disabled="tickets_bought === 0"> Return ticket </button>-->
<!--    <h4> Total tickets bought: {{ tickets_bought }} </h4>-->
<!--    <h4> Remaining tickets: {{ remaining_tickets }} </h4>-->
<!--    <h4> Match price: {{ price_match }} </h4>-->
<!--    <h4> Money available: {{ money_available }} </h4>-->
      <div class="header borderBottom">
      <div class="row col-left">
        <div class="col">
          <h1 style="text-align: start" class="size">{{ message }}</h1>
        </div>
        <div class="col teAlign-marRigth">
          <div class="icon-button-container">
            <img src="../assets/person-icon.png" alt="Person Icon" width="24" height="24" style="margin-right: 2px;" class="mb-1">
            <span class="spanText" style="margin-right: 13px;">
              {{  this.$route.query.username === undefined ? 'test' : this.$route.query.username }}
            </span>
            <img src="../assets/money-icon.png" alt="Money Icon" width="24" height="24" style="margin-right: 2px;">
            <span class="spanText" style="margin-right: 13px;">
              {{this.$route.query.username === undefined ? '50.75$' : '200$'}}
            </span>
            <button class="btn btn-outline-primary" @click="veureCistella()" :style="buttonStyle" style="margin-right: 13px;">
              {{ showCart ? 'Tanca cistella' : 'Veure cistella' }}
              <span style="margin-left: 5px;">({{ totalTickets }})</span>
            </button>
            <button class="btn button-secondary" @click="goLogin()">
              {{this.$route.query.username === undefined ? 'Log In' : 'Log Out'}}
            </button>
          </div>
        </div>
      </div>
    </div>
       <div class="body colorSecondary min-height">
          <div v-if="showCart" class="margins">
            <div class="colorSecondary margin-top"></div>
            <div class="colorWhite">
              <span>CART</span>
            <table class="table" v-if="showCart">
              <thead>
                <tr>
                  <th>Sport</th>
                  <th>Competition</th>
                  <th>Match</th>
                  <th>Quantity</th>
                  <th>Price(&euro;)</th>
                  <th>Total</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <!-- Aquí debes iterar sobre los elementos de la cistella y mostrarlos en filas -->
                <tr v-for="(match) in matches_added" :key="match.id">
                  <td>{{match.competition.sport}}</td>
                  <td>{{match.competition.name}}</td>
                  <td>{{match.local.name}} - {{match.visitor.name}}
                  <td>
                    {{match.ticketCount}}
                    <button class="btn btn-outline-danger" @click="decreaseTickets(match)" :disabled="match.ticketCount < 1"> - </button>
                    <button class="btn btn-success" @click="increaseTickets(match)" :disabled="match.total_available_tickets === 0"> + </button>
                  </td>
                  <td>{{match.price}}</td>
                  <td>{{(match.price * match.ticketCount).toFixed(2)}}</td>
                  <td><button class="btn btn-outline-danger" @click="removeEventOfCart(match)"> Eliminar entrada </button></td>
              </tbody>
            </table>
            <button v-if="matches_added.length >= 0" class="btn btn-secondary" @click="veureCistella()"> Enrere </button>
            <button v-if="matches_added.length >= 0" class="btn btn-success"  @click="finalizePurchase()" :disabled="matches_added.length <= 0"> Finalitzar la compra </button>
            <p v-else>Your cart is currently empty.</p>
            </div>
          </div>
              <div v-else class="row card-container">
                <div class="col-lg-4 col-md-6 mb-4" v-for="(match) in matches" :key="match.id">
                  <br>
                  <div class="card" style="width: 18rem;">
                    <img class="card-img-top" :src='require("../assets/" + match.competition.sport +".jpg")' alt="Card image cap">
                    <div class="card-body">
                      <h5>{{ match.competition.sport }} - {{ match.competition.category }}</h5>
                      <h6>{{ match.competition.name }}</h6>
                      <h6><strong>{{ match.local.name }}</strong> ({{ match.local.country }}) vs <strong>{{ match.visitor.name }}</strong> ({{ match.visitor.country }})</h6>
                      <h6>{{ match.date.substring(0,10) }}</h6>
                      <h6>{{ match.price }} &euro;</h6>
                      <h6> Entrades disponibles: {{ match.total_available_tickets }}</h6>
                      <button class="btn btn-success"  @click="addEventToCart(match)">Afegeix a la cistella</button>
                    </div>
                  </div>
                </div>
              </div>

      </div>
  </div>

</template>
<head>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
</head>
<style>
  .container {
    background-color: white;
  }
  h1.size{
    font-size: 50px;
    color: black;
    font-family: inherit;
  }
  .borderBottom{
    border-bottom: 2px solid black;
  }
  .card-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-left: 125px; /* Ajusta el margen izquierdo según tus necesidades */
  }
  .min-height{
    min-height: 599px;
  }
  .colorSecondary {
    background-color: #ede1d6d4;
  }
  .colorWhite{
    background-color: white;
  }
  .margins{
    margin: 0px 200px 0px 200px;
  }
  .margin-top {
    height: 50px; /* Altura del margen superior */
  }
  .col-left {
    margin-left: 145px; /* Margen izquierdo */
    margin-bottom: 25px;
    margin-top: 12px;
  }
  .button-secondary{
    color: #28a745;
      background-color: #fff;
      border-color: #28a745;
  }
  .teAlign-marRigth{
    text-align: right;
    margin-right: 160px;
  }
  .spanText{
    font-weight: bold;
    font-family: cursive;
    font-size: 16px;
  }
  .icon-button-container {
    display: flex;
    align-items: center; /* Alinear verticalmente los elementos */
    margin-right: 50px;
    justify-content: flex-end;
  }
</style>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      message: 'Sport matches ',
      user: this.username,
      tickets_bought: 0,
      remaining_tickets: 15,
      money_available: 100,
      price_match: 10,
      showCart: false,
      matches: [],
      matches_added: [],
      creatingAccount: false,
      is_admin: false,
      totalTickets: 0,
    }
  },
  computed: {
  totalTickets() {
    return this.matches_added.reduce((total, match) => total + match.ticketCount, 0);
  },
  },
  methods: {
    buyTicket () {
      if (this.remaining_tickets > 0 && this.money_available >= this.price_match) {
        this.tickets_bought += 1
        this.remaining_tickets -= 1
        this.money_available -= this.price_match
      }
    },
    goLogin () {
      this.$router.push('/userlogin')
    },
    veureCistella () {
      this.showCart = !this.showCart
      console.log(this.username)
      this.getMatches()
    },
    returnTicket () {
      if (this.tickets_bought > 0) {
        this.tickets_bought -= 1
        this.remaining_tickets += 1
        this.money_available += this.price_match
      }
    },
    decreaseTickets (match) {
      if (match.total_available_tickets > 0 && match.ticketCount > 0) {
        match.total_available_tickets += 1
        match.ticketCount -= 1
        this.totalTickets -= 1;
      }
    },
    increaseTickets (match) {
      match.total_available_tickets -= 1
      match.ticketCount += 1
      this.totalTickets += 1;
    },
    addEventToCart (match) {
      const existingMatch = this.matches_added.find((addedMatch) => addedMatch.id === match.id)
      if (!existingMatch) {
        match.ticketCount = 1
        this.totalTickets += 1;
        this.matches_added.push(match)
      }
    },
    removeEventOfCart (match) {
      const index = this.matches_added.indexOf(match)
      if (index !== -1) {
        this.totalTickets -= match.ticketCount;
        this.matches_added.splice(index, 1)
      }
    },
    finalizePurchase () {
      console.log('Finalize Purchase clicked')
      for (let i = 0; i < this.matches_added.length; i += 1) {
        const parameters = {
          match_id: this.matches_added[i].id,
          tickets_bought: this.matches_added[i].ticketCount
        }
        this.addPurchase(parameters)
      }
    },
    addPurchase (parameters) {
      console.log('addPurchase achieved')
      const path = 'http://localhost:8000/orders/Oscar'
      // 5.5 seguretat (no va)
      // const path = 'http://localhost:8000/orders/' + this.username
      // const config = {
      //   headers: {
      //     Authorization: 'Bearer ' + this.token
      //   }
      // }
      // axios.post(path, parameters, config)
      axios.post(path, parameters)
        .then(() => {
          console.log('Order done')
          this.matches_added.splice(0)
          this.matches_added = []
          this.showCart = !this.showCart
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getMatches()
        })
    },
    getMatches () {
      const pathMatches = 'http://localhost:8000/matches/'
      const pathCompetition = 'http://localhost:8000/competitions/'

      axios.get(pathMatches)
        .then((res) => {
          var matches = res.data.filter((match) => {
            return match.competition.name != null
          })
          var promises = []
          for (let i = 0; i < matches.length; i++) {
            const promise = axios.get(pathCompetition + matches[i].competition.name)
              .then((resCompetition) => {
                delete matches[i].competition.name
                matches[i].competition = {
                  'name': resCompetition.data.competition.name,
                  'category': resCompetition.data.competition.category,
                  'sport': resCompetition.data.competition.sport
                }
                matches[i].total_available_tickets = resCompetition.data.total_available_tickets
              })
              .catch((error) => {
                console.error(error)
              })
            promises.push(promise)
          }
          Promise.all(promises).then((_) => {
            this.matches = matches
          })
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 5.3
    getAccount () {
      // Realizar solicitud GET al backend para obtener la información de la cuenta del usuario
      // actualment no funciona
      // const path = 'http://localhost:8000/account/' + this.username
      // utilitzar de moment aquesthardcodejat
      const path = 'http://localhost:8000/account/Oscar'
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
  },
  created () {
    this.getMatches()
    this.logged = this.$route.query.logged === 'true'
    this.username = this.$route.query.username
    console.log(this.$route)
    console.log(this.$route.query)
    console.log(this.$route.query.username)
    this.token = this.$route.query.token
    if (this.logged === undefined) {
      this.logged = false
    }
    this.getAccount()
  }
}
</script>
