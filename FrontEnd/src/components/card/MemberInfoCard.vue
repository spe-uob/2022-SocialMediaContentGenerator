<template>
  <q-card>
    <q-item>
      <q-item-section avatar>
        <q-avatar size="60px" class="shadow-10">
          <img :src="avatar">
        </q-avatar>
      </q-item-section>

      <q-item-section>
        <q-item-label class="text-grey-8 text-weight-bold">{{ name }}</q-item-label>
        <q-item-label caption>
          {{ contact }}
        </q-item-label>
        <q-item-label class="text-grey-8">
          {{ disc }}
        </q-item-label>
      </q-item-section>

      <q-item-section side>
        <q-item-label>
          <q-btn size="sm" flat round icon="fab fa-facebook" class="bg-indigo-7 text-white"/>
        </q-item-label>
        <q-item-label>
          <q-btn size="sm" flat round icon="fab fa-twitter" class="bg-info text-white"/>
        </q-item-label>

      </q-item-section>
    </q-item>

    <q-separator></q-separator>
    <q-card-section>
      <div class="q-pa-sm text-grey-8">
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "MemberInfoCard",
  props: ['id','avatar','name','contact','disc']
}
</script>

<style scoped>

</style>
