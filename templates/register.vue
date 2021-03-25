{% extends "layout.html" %}
{% block content %}
    <br><br><br>

    <div id="app">
        <v-app id="inspire">

            <div class="jumbotron">
                <v-container>
                    <v-card
                            class="mx-auto"
                            width="70%"
                    >
                        <v-img
                                src="/static/images/cover.jpg"
                                width="100%"
                        >
                        </v-img>

                        <v-card-title>
                            Create your account
                        </v-card-title>

                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col
                                            cols="6"
                                            small="6"
                                    >
                                        <v-form v-model="valid"
                                                ref="form"
                                                lazy-validation
                                        >
                                            <v-text-field
                                                    v-model="formElements.email"
                                                    class="rounded-pill"
                                                    outlined
                                                    clearable
                                                    dense
                                                    label="Email"
                                                    required
                                                    :rules="validEmail"
                                            >
                                            </v-text-field>


                                            <v-text-field
                                                    v-model="formElements.username"
                                                    class="rounded-pill"
                                                    outlined
                                                    clearable
                                                    dense
                                                    label="Username"
                                                    required
                                                    :rules="validOther"
                                            >
                                            </v-text-field>



                                            <v-text-field
                                                    v-model="formElements.password"
                                                    class="rounded-pill"
                                                    outlined
                                                    clearable
                                                    dense
                                                    label="Password"
                                                    required
                                                    type="password"
                                                    :rules="validPassword"
                                            >
                                            </v-text-field>


                                            <v-file-input
                                                    @change="previewImage"
                                                    accept="image/*"
                                                    v-model="imgFile"
                                                    class="rounded-pill"
                                                    label="Image Profile"
                                                    clearable
                                                    outlined
                                                    required
                                                    dense
                                                    :rules="validOther"
                                            >
                                                <template v-slot:selection="{ text }">
                                                    <v-chip
                                                            small
                                                            label
                                                            color="primary"
                                                    >
                                                        [[ text ]]
                                                    </v-chip>
                                                </template>
                                            </v-file-input>


                                            <v-img
                                                    :src="url"
                                            >

                                            </v-img>

                                            <v-row style="margin-top: 20px">
                                                <v-btn
                                                        :disabled="!valid"
                                                        color="red"
                                                        class="rounded-pill text-white"
                                                        @click="submit"
                                                        :loading="!btnSpinner"
                                                >
                                                    Sign Up
                                                </v-btn>
                                                <p style="margin-top: 10px"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Have an
                                                    account? <a href="/root_login" class="text-danger">Log in now</a>
                                                </p>
                                            </v-row>
                                        </v-form>
                                    </v-col>
                                    <v-col
                                            cols="6"
                                            small="6"
                                    >

                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card-text>
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
                validPassword: [
                    v => !!v || 'Please Input',
                    v => v && v.length >= 6 || 'Password must be at least 6 characters long'
                ],
                validOther: [v => !!v || 'Please input'],
                imgFile: null,
                formElements: {
                    email: '',
                    username: '',
                    password: ''
                },
                btnSpinner: true,
                valid: false,
                url: null,
                items: [
                    {
                        src: '/static/images/iot1.png'
                    },
                    {
                        src: '/static/images/41002.jpg'
                    }
                ]
            }),
            methods: {
                previewImage() {
                    this.url = URL.createObjectURL(this.imgFile);
                },
                submit() {
                    let form = this.$refs.form.validate();
                    if (form === true) {
                        this.btnSpinner = false;
                        let formData = new FormData();
                        formData.append('file', this.imgFile);
                        formData.append('email', this.formElements.email);
                        formData.append('username', this.formElements.username);
                        formData.append('password', this.formElements.password);
                        axios.post('/secure/register', formData,
                            {
                                headers: {
                                    'Content-Type': 'multipart/form-data',
                                    'X-Token': 'secure'
                                }
                            })
                            .then((res) => {
                                console.log(res.data)
                                this.btnSpinner = true;
                                Swal.fire({
                                    icon: 'success',
                                    title: 'Sign In Success',
                                    showConfirmButton: false,
                                    timer: 1500
                                })
                                .then(() => {
                                    window.location = '/root_login'
                                })
                            })
                            .catch((err) => {
                                console.error(err);
                            })
                    }
                },
            },
            delimiters: ["[[", "]]"]
        })
    </script>


{% endblock %}