import { mount, shallowMount } from '@vue/test-utils'
import Twitter from './../src/pages/Twitter.vue'

describe('Twitter Test', () => {
  it('should not be initialized with access token', () => {
    expect(Twitter.data().access_token).toMatch('')
  })
  it('should not be initialized with access secret', () => {
    expect(Twitter.data().access_token).toMatch('')
  })
})
