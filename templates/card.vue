{% extends "layout.html" %}
{% block content %}
  <br>
  <br>
  <div id="app">
    <v-container>
      <v-row>
        <v-col cols="3">
          <div class="text-center">
            <v-avatar>
              <img
                  :src="auth.picture"
                  alt="attr"
              >
            </v-avatar>
            <h4>[[auth.name]]</h4>
            <p>Click: [[count]]</p>
            <p>My Best: [[my_best]]</p>
            <p>Global Best: [[global_best]]</p>

          </div>

        </v-col>
        <v-col cols="9">
          <v-row
          >
            <v-col
                v-for="(card, objKey) in memoryCards"
                :key="card"
                cols="12"
                md="3"
                class="col-auto mb-5 flip-container"
                :class="{ 'flipped': card.flipped, 'matched' : card.matching }"
            >
              Card: [[objKey + 1]]
              <div class="front border rounded shadow" @click="flipCard(card)">
                <img width="180" height="220"
                     src="/static/images/card%20back%20orange.png">
              </div>
              <div class="back rounded border">
                <img width="200" height="220" :src="'/static/images/'+card.img">
              </div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      {#      <v-row justify="space-around">#}
      {#        <div class="row justify-content-md-center">#}
      {#          <div v-for="card in memoryCards" class="col-auto mb-3 flip-container"#}
      {#               :class="{ 'flipped': card.isFlipped, 'matched' : card.isMatched }"#}
      {#               @click="flipCard(card)">#}
      {#            <div class="memorycard">#}
      {#              <div class="front border rounded shadow"><img width="100" height="150"#}
      {#                                                            src="/static/images/card%20back%20orange.png"></div>#}
      {#              <div class="back rounded border"><img width="100" height="150" :src="'/static/images/'+card.img">#}
      {#              </div>#}
      {#            </div>#}
      {#          </div>#}
      {#        </div>#}
      {#      </v-row>#}
    </v-container>
  </div>


  <script>
      let app = new Vue({
          el: '#app',
          data: {
              count: 0,
              global_best: 0,
              global_user: '',
              my_best: 0,
              memoryCards: [],
              flippedCards: [],
              cards: [],
              auth: null
          },
          beforeMount() {
              let pusher = new Pusher('0e4e34e901bbfddd5557', {
                  cluster: 'us2'
              });
              let channel = pusher.subscribe('secure');
              channel.bind('session', data => {
                  this.auth = data
              });
          },
          created() {
              this.getSocket();
              const path = '/secure/socket_auth';
              axios.get(path)
                  .then((res) => {
                      this.auth = res.data;
                      const path = `/card/create_card/${this.auth.name}`;
                      axios.get(path)
                          .then((res) => {
                              this.my_best = res.data.my_best
                              this.cards = res.data.cards;
                              this.global_best = res.data.best;
                              this.cards.forEach((card) => {
                                  Vue.set(card, 'flipped', false);
                                  Vue.set(card, 'matching', false);
                              });
                              this.memoryCards = _.shuffle(this.memoryCards.concat(_.cloneDeep(this.cards), _.cloneDeep(this.cards)));
                          })
                          .catch((err) => {
                              console.error(err);
                          })
                      console.log(false);
                  })
                  .catch((err) => {
                      console.error(err);
                  })
          },
          methods: {
              getSocket() {

              },
              flipCard(card) {
                  console.log(card)
                  if (card.matching || card.flipped || this.flippedCards.length === 2)
                      return;

                  card.flipped = true;
                  this.updateCard(false, card.id)
                  if (this.flippedCards.length < 2)
                      this.flippedCards.push(card);
                  if (this.flippedCards.length === 2)
                      this._match(card);
              },
              _match(card) {
                  console.log(card)
                  if (this.flippedCards[0].name === this.flippedCards[1].name) {
                      setTimeout(() => {
                          this.flippedCards.forEach(card => card.matching = true);
                          this.sendFlipped(true, card.id)
                          this.flippedCards = [];
                      }, 400);
                  } else {
                      setTimeout(() => {
                          this.flippedCards.forEach((card) => {
                              card.flipped = false
                          });
                          this.flippedCards = [];
                      }, 800);
                  }
              },
              sendFlipped(query, index) {
                  this.id_card = $cookies.get('id_card')
                  let data = {'query': query, 'index': index, 'id': this.id_card, 'global': this.auth.name}
                  const path = `card/flippedCard`
                  axios.post(path, data)
                      .then((res) => {
                          this.global_best = res.data.best;
                          console.log('success')
                      })
                      .catch((err) => {
                          console.error(err);
                      })
              },
              updateCard(query, index) {
                  this.id_card = $cookies.get('id_card')
                  let data = {'query': query, 'index': index, 'id': this.id_card, 'num': 1, 'global': this.auth.name}
                  const path = `card/updateCard`
                  axios.post(path, data)
                      .then((res) => {
                          this.count = res.data.num;
                      })
                      .catch((err) => {
                          console.error(err);
                      })
              },
              getFlipped(id) {
                  const path = `card/getFlipped/${id}`;
                  axios.get(path)
                      .then((res) => {

                      })
                      .catch((err) => {
                          console.error(err)
                      })
              }

          },
          delimiters: ['[[', ']]']
      });

  </script>


  <style>
      .flip-container {
          -webkit-perspective: 1000;
          -moz-perspective: 1000;
          -o-perspective: 1000;
          perspective: 1000;
          min-height: 120px;
          cursor: pointer;
      }

      .front,
      .back {
          -webkit-backface-visibility: hidden;
          -moz-backface-visibility: hidden;
          -o-backface-visibility: hidden;
          backface-visibility: hidden;
          -webkit-transition: 0.6s;
          -webkit-transform-style: preserve-3d;
          -moz-transition: 0.6s;
          -moz-transform-style: preserve-3d;
          -o-transition: 0.6s;
          -o-transform-style: preserve-3d;
          -ms-transition: 0.6s;
          -ms-transform-style: preserve-3d;
          transition: 0.6s;
          transform-style: preserve-3d;
          top: 0;
          left: 0;
          width: 100%;
      }

      .back {
          -webkit-transform: rotateY(-180deg);
          -moz-transform: rotateY(-180deg);
          -o-transform: rotateY(-180deg);
          -ms-transform: rotateY(-180deg);
          transform: rotateY(-180deg);
          position: absolute;
      }

      .flip-container.flipped .back {
          -webkit-transform: rotateY(0deg);
          -moz-transform: rotateY(0deg);
          -o-transform: rotateY(0deg);
          -ms-transform: rotateY(0deg);
          transform: rotateY(0deg);
      }

      .flip-container.flipped .front {
          -webkit-transform: rotateY(180deg);
          -moz-transform: rotateY(180deg);
          -o-transform: rotateY(180deg);
          -ms-transform: rotateY(180deg);
          transform: rotateY(180deg);
      }

      .matched {
          opacity: 0.3;
      }
  </style>


{% endblock %}