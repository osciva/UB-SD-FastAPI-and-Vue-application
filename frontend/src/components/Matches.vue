<template>
  <div id="app">
    <h1> {{ message }} </h1>
    <button class="btn btn-success btn-lg" @click="buyTicket" :disabled="money_available < price_match"> Buy ticket </button>
    <button class="btn btn-danger btn-lg" @click="returnTicket" :disabled="tickets_bought === 0"> Return ticket </button>
    <h4> Total tickets bought: {{ tickets_bought }} </h4>
    <h4> Remaining tickets: {{ remaining_tickets }} </h4>
    <h4> Match price: {{ price_match }} </h4>
    <h4> Money available: {{ money_available }} </h4>

    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-md-6 mb-4" v-for="(match) in matches" :key="match.id">
          <br>
          <div class="card" style="width: 18rem;">
            <img class="card-img-top" :src="getMatchImage(match.competition.sport)" alt="Card image cap">
            <div class="card-body">
              <h5>{{ match.competition.sport }} - {{ match.competition.category }}</h5>
              <h6>{{ match.competition.name }}</h6>
              <h6><strong>{{ match.local.name }}</strong> ({{ match.local.country }}) vs <strong>{{ match.visitor.name }}</strong> ({{ match.visitor.country }})</h6>
              <h6>{{ match.date.substring(0,10) }}</h6>
              <h6>{{ match.price }} &euro;</h6>
              <button class="btn btn-success" @click="addEventToCart(match)">Afegeix a la cistella</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      message: 'My first component',
      tickets_bought: 0,
      remaining_tickets: 15,
      money_available: 100,
      price_match: 10,
      matches: [
  {
    'id': 1,
    'local': {
      'id': 3,
      'name': 'Club Juventut Les Corts',
      'country': 'Spain'
    },
    'visitor': {
      'id': 2,
      'name': 'CE Sabadell',
      'country': 'Spain'
    },
    'competition': {
      'name': 'Women\'s European Championship',
      'category': 'Senior',
      'sport': 'Volleyball'
    },
    'date': '2022-10-12T00:00:00',
    'price': 4.3
  },
  {
    'id': 2,
    'local': {
      'id': 3,
      'name': 'Club Juventut Les Corts',
      'country': 'Spain'
    },
    'visitor': {
      'id': 2,
      'name': 'CE Sabadell',
      'country': 'Spain'
    },
    'competition': {
      'name': '1st Division League',
      'category': 'Junior',
      'sport': 'Futsal'
    },
    'date': '2022-07-10T00:00:00',
    'price': 129.29
  },
  {
    'id': 3,
    'local': {
      'id': 1,
      'name': 'CV Vall D\'Hebron',
      'country': 'Spain'
    },
    'visitor': {
      'id': 4,
      'name': 'Volei Rubi',
      'country': 'Spain'
    },
    'competition': {
      'name': '1st Division League',
      'category': 'Junior',
      'sport': 'Futsal'
    },
    'date': '2022-08-10T00:00:00',
    'price': 111.1
  }
],
      matches_added: []
    }

  },
  methods: {
    buyTicket () {
      if (this.remaining_tickets > 0 && this.money_available >= this.price_match) {
        this.tickets_bought += 1
        this.remaining_tickets -= 1
        this.money_available -= this.price_match
      }
    },
    returnTicket () {
      if (this.tickets_bought > 0) {
        this.tickets_bought -= 1
        this.remaining_tickets += 1
        this.money_available += this.price_match
      }
    },
    addEventToCart (match) {
      this.matches_added.push(match)
    },
    getMatchImage(sport) {
      if (sport === 'Volleyball') {
        return '../assets/volei1.jpg';
      } else if (sport === 'Futsal') {
        return "../assets/futsal1.jpg";
      } else {
        // si no hay imagen definida para el deporte, se muestra una imagen genérica
        return '../assets/default.jpg';
      }
    }

  }
}

</script>
