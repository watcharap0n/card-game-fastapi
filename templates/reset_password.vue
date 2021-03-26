{% extends "layout.html" %}
{% block content %}



  <br><br><br><br><br>
  <div id="app">

    <v-app id="inspire">
      <div class="text-center">
        <h2>Reset your password</h2>

        To reset your password, enter your email below and submit. An email will be sent to you with instructions about
        how to complete the process.
        <br>
        <br>
      </div>
      <div class="jumbotron">
        <v-container>
          <v-form v-model="valid"
                  ref="form"
                  lazy-validation
          >
            <v-spacer></v-spacer>
            <v-text-field
                label="Reset Password"
                placeholder="Enter your email"
                outlined
                :rules="validEmail"
                v-model="email"
            ></v-text-field>
            <v-btn
                color="success"
                class="mr-4 rounded-pill text-white"
                @click="submit"
                :loading="!btnSpinner"
            >
              Submit
            </v-btn>
          </v-form>
        </v-container>
      </div>
    </v-app>
  </div>



  <script>
      new Vue({
          el: '#app',
          vuetify: new Vuetify(),
          data: {
              email: '',
              validEmail: [
                  v => !!v || 'Invalid Email',
                  v => /.+@.+\..+/.test(v) || 'Please input your email valid',
              ],
              valid: false,
              btnSpinner: true,
          },
          methods: {

              submit() {
                  let form = this.$refs.form.validate();
                  if (form === true) {
                      this.btnSpinner = false;
                      let formData = new FormData();
                      formData.append('email', this.email);
                      axios.post('/secure/forgot_password', formData)
                          .then(() => {
                              this.btnSpinner = true;
                              Swal.fire({
                                  icon: 'success',
                                  title: 'Please check your email',
                              })
                          })
                          .catch((err) => {
                              console.error(err);
                          })
                  }
              },
          }

      })
  </script>

{% endblock %}