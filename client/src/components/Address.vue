<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Addresss</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.address-modal>Add Address</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Address</th>
              <th scope="col">Name</th>
              <th scope="col">Visited?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(address, index) in addresss" :key="index">
              <td>{{ address.address }}</td>
              <td>{{ address.name }}</td>
              <td>
                <span v-if="address.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.address-update-modal
                          @click="editAddress(address)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteAddress(address)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addAddressModal"
            id="address-modal"
            address="Add a new address"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-address-group"
                    label="Title:"
                    label-for="form-address-input">
          <b-form-input id="form-address-input"
                        type="text"
                        v-model="addAddressForm.address"
                        required
                        placeholder="Enter address">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-name-group"
                      label="Author:"
                      label-for="form-name-input">
            <b-form-input id="form-name-input"
                          type="text"
                          v-model="addAddressForm.name"
                          required
                          placeholder="Enter name">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addAddressForm.read" id="form-checks">
            <b-form-checkbox value="true">Visited?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editAddressModal"
            id="address-update-modal"
            address="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-address-edit-group"
                    label="Title:"
                    label-for="form-address-edit-input">
          <b-form-input id="form-address-edit-input"
                        type="text"
                        v-model="editForm.address"
                        required
                        placeholder="Enter address">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-name-edit-group"
                      label="Author:"
                      label-for="form-name-edit-input">
            <b-form-input id="form-name-edit-input"
                          type="text"
                          v-model="editForm.name"
                          required
                          placeholder="Enter name">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-edit-group">
          <b-form-checkbox-group v-model="editForm.read" id="form-checks">
            <b-form-checkbox value="true">Visited?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      addresss: [],
      addAddressForm: {
        address: '',
        name: '',
        read: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        address: '',
        name: '',
        read: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getAddresss() {
      const path = 'http://localhost:5000/addresss';
      axios.get(path)
        .then((res) => {
          this.addresss = res.data.addresss;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addAddress(payload) {
      const path = 'http://localhost:5000/addresss';
      axios.post(path, payload)
        .then(() => {
          this.getAddresss();
          this.message = 'Address added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getAddresss();
        });
    },
    initForm() {
      this.addAddressForm.address = '';
      this.addAddressForm.name = '';
      this.addAddressForm.read = [];
      this.editForm.id = '';
      this.editForm.address = '';
      this.editForm.name = '';
      this.editForm.read = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addAddressModal.hide();
      let read = false;
      if (this.addAddressForm.read[0]) read = true;
      const payload = {
        address: this.addAddressForm.address,
        name: this.addAddressForm.name,
        read, // property shorthand
      };
      this.addAddress(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addAddressModal.hide();
      this.initForm();
    },
    editAddress(address) {
      this.editForm = address;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAddressModal.hide();
      let read = false;
      if (this.editForm.read[0]) read = true;
      const payload = {
        address: this.editForm.address,
        name: this.editForm.name,
        read,
      };
      this.updateAddress(payload, this.editForm.id);
    },
    updateAddress(payload, addressID) {
      const path = `http://localhost:5000/addresss/${addressID}`;
      axios.put(path, payload)
        .then(() => {
          this.getAddresss();
          this.message = 'Address updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAddresss();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAddressModal.hide();
      this.initForm();
      this.getAddresss(); // why?
    },
    removeAddress(addressID) {
      const path = `http://localhost:5000/addresss/${addressID}`;
      axios.delete(path)
        .then(() => {
          this.getAddresss();
          this.message = 'Address removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAddresss();
        });
    },
    onDeleteAddress(address) {
      this.removeAddress(address.id);
    },
  },
  created() {
    this.getAddresss();
  },
};
</script>
