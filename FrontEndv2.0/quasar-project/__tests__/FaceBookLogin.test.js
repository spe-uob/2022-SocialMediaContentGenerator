import { shallowMount } from '@vue/test-utils'
import 'firebase/auth'


import AuthComponent from './../src/components/FBAuthComponent.vue'

describe('AuthComponent Test', () => {
  it('should render a button with text: sign in with facebook', () => {
    const wrapper = shallowMount(AuthComponent)
    const button = wrapper.find("q-btn")
    expect(button.exists).toBeTruthy
    expect(button.html()).toContain('sign in with facebook')
  })
})
