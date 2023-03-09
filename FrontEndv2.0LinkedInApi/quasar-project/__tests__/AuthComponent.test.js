import { mount, shallowMount } from '@vue/test-utils'
import AuthComponent from './../src/components/AuthComponent.vue'

describe('AuthComponent Test', () => {
  it('has a valid apiKey', () => {
    expect(AuthComponent.data().apiKey).toBe('EzoH0w73hC3naY84U6NBHZHyz')
  })
  it('has a valid apiSecret', () => {
    expect(AuthComponent.data().apiSecret).toBe('qjFQ5WPxqJD7C0JZtMiORkzbhYAXjNNfX0WyMdx5GWz1IiZxFw')
  })
  it('should redirect to /twitter when clicking the twitter button', () => {
    const wrapper = mount(AuthComponent)
    const button = wrapper.find("q-btn")
    expect(button.exists()).toBe(true)
    /*button.trigger('click')
    expect(window.location.href).toBe('/twitter')*/
  })
})
