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
          {{ disc }}
        </q-item-label>
        <q-item-label class="text-grey-8">
          {{ contact }}
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

  </q-card>
</template>

<script>
import {defineComponent} from "vue";

export default defineComponent({
  name: "MemberInfoCard",
  props: ['id','avatar','name','contact','disc']
})
</script>

<style scoped>

</style>
