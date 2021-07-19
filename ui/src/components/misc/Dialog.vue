
<template>
  <el-dialog :title="prop.dialogTitle" v-model="showDialog" width="30%" center>
    <span>{{ prop.dialogMessage }}</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="$emit('userRejected')">Cancel</el-button>
        <el-button type="info" @click="$emit('userConfirmed')"
          >Confirm</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>

<script>
export default {
  mounted() {
    console.log("dialog compnent mounted");
  },
  emits: ["userRejected", "userConfirmed"],
  props: {
    prop: {
      type: Object,
    },
  },
  data() {
    return {};
  },

  computed: {
    showDiaog: function () {
      return this.prop.showDiaog;
    },
  },
};
</script>

<style>
</style>
