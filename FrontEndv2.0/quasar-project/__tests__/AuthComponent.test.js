import { mount, shallowMount } from '@vue/test-utils'
import firebase from 'firebase/app'
import 'firebase/auth'
import AuthComponent from './../src/components/AuthComponent.vue'
import { TwitterAuthProvider } from 'firebase/auth';

jest.mock('firebase/auth', () => {
  const originalModule = jest.requireActual('firebase/auth');
  const mockAuthProvider = jest.fn(() => ({
    providerId: originalModule.TwitterAuthProvider.PROVIDER_ID,
  }));
  return {
    ...originalModule,
    TwitterAuthProvider: mockAuthProvider,
  };
});

const provider = new TwitterAuthProvider();
expect(provider.providerId).toBe('twitter.com');

describe('AuthComponent Test', () => {
  it('has a valid apiKey', () => {
    expect(AuthComponent.data().apiKey).toBe('EzoH0w73hC3naY84U6NBHZHyz')
  })
  it('has a valid apiSecret', () => {
    expect(AuthComponent.data().apiSecret).toBe('qjFQ5WPxqJD7C0JZtMiORkzbhYAXjNNfX0WyMdx5GWz1IiZxFw')
  })
  it('should render a button with text: sign in with twitter', () => {
    const wrapper = shallowMount(AuthComponent)
    const button = wrapper.find("q-btn")
    expect(button.exists).toBeTruthy
    expect(button.html()).toContain('sign in with twitter')
  })
  it('logs in a user with Twitter successfully', async () => {
    const wrapper = mount(AuthComponent)
    const loginButton = wrapper.find('q-btn')
    await loginButton.trigger('click')
    expect(firebase.auth().signInWithPopup).toHaveBeenCalledWith(expect.any(firebase.auth.TwitterAuthProvider))
    expect(wrapper.vm.$data.isLoggedIn).toBe(true)
  })
})
