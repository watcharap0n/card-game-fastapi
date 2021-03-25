{% extends "layout.html" %}
{% block content %}
  <br><br><br>

  <div id="app">
    <v-app id="inspire">

      <div class="jumbotron">
        <v-container>
          <v-card
              class="mx-auto"
              width="100%"
          >
            <v-row justify="center"
            >
              <v-col small="6"
                     cols="6"
              >

                <v-carousel
                    width="100%"
                    height="100%"
                    cycle
                    hide-delimeter-background
                    show-arrows-on-hover
                >
                  <v-carousel-item
                      v-for="(item, i) in items"
                      :key="i"
                      :src="item.src"
                  >
                  </v-carousel-item>
                </v-carousel>


              </v-col
              >

              <v-col
                  cols="6"
                  small="6"
              >
                <div
                    class="text-center"
                >
                  <h2>Welcome</h2>
                  <h6>Please Sign In</h6>
                  <v-container>
                    <v-form v-model="valid"
                            ref="form"
                            lazy-validation
                    >
                      <v-text-field
                          v-model="email"
                          class="rounded-pill"
                          outlined
                          clearable
                          dense
                          label="Email"
                          :rules="validEmail"
                          required
                      >
                      </v-text-field>


                      <v-text-field
                          v-model="password"
                          class="rounded-pill"
                          outlined
                          clearable
                          dense
                          type="password"
                          label="Password"
                          :rules="validOther"
                          required
                      >
                      </v-text-field>

                      <v-checkbox
                          v-model="remember"
                          style="margin-top: -12px; margin-bottom: 10px"
                          label="remember me"
                          color="red"
                          value="checked"
                          hide-details
                      >
                      </v-checkbox>
                      <v-btn
                          block
                          color="red"
                          class="mr-4 rounded-pill text-white"
                          @click="submit"
                          :loading="!btnSpinner"
                      >
                        Submit
                      </v-btn>
                      <div class="text-center"
                           style="margin-top: 10px"
                      >
                        <p>
                          Dont' have an account? <a href="/root_register">Sign In</a>
                        </p>
                        <p>
                          Forgot Password
                        </p>
                      </div>
                    </v-form>
                  </v-container>
                </div>

              </v-col>
            </v-row>

          </v-card>
        </v-container>
      </div>

    </v-app>
  </div>



  <script>
      new Vue({
          el: '#app',
          vuetify: new Vuetify(),
          data: () => ({
              validEmail: [
                  v => !!v || 'Invalid Email',
                  v => /.+@.+\..+/.test(v) || 'Please input your email valid',
              ],
              validOther: [v => !!v || 'Please input your password'],
              items: [
                  {
                      src: '/static/images/game1.png'
                  },
                  {
                      src: '/static/images/game2.png'
                  }
              ],
              valid: false,
              btnSpinner: true,
              email: '',
              password: '',
              remember: null,
              headerX: '',
          }),
          beforeCreate() {
              const path = '/secure/cookie_login';
              axios.get(path)
                  .then((res) => {
                      if (res.data.email) {
                          this.email = res.data.email
                          this.password = res.data.password
                      }
                  })
                  .catch((err) => {
                      console.error(err)
                  })
          },
          methods: {
              submit() {
                  let form = this.$refs.form.validate();
                  if (form === true) {
                      this.btnSpinner = false;
                      let formData = new FormData();
                      formData.append('username', this.email)
                      formData.append('password', this.password)
                      formData.append('remember', this.remember)
                      axios.post('/secure/login', formData,
                          {
                              headers: {
                                  'Content-Type': 'multipart/form-data',
                              }
                          }
                      )
                          .then((res) => {
                              this.btnSpinner = true;
                              let status = res.data.status;
                              let fg = res.data.fg;
                              console.log(fg)
                              if (fg) {
                                  Swal.fire({
                                      icon: 'info',
                                      title: 'Please check your email to verify your account',
                                  })
                              } else {
                                  if (status === true) {
                                      window.location = '/card'
                                  } else {
                                      Swal.fire({
                                          icon: 'error',
                                          title: 'Email or Password Invalid',
                                          text: 'Please provide a valid email and password!',
                                          footer: '<a href="/root_register">you dont have an account? </a>'
                                      })
                                  }
                              }
                          })
                          .catch((err) => {
                              console.error(err);
                          })
                  }
              }
          },
          delimiters: ["[[", "]]"]
      })
  </script>


{% endblock %}