<template>
    <div class="max-w-md w-full mx-auto min-h-screen flex items-center justify-center flex-col" dir="rtl">
        <div class="text-center">
            <h2 class="mt-6 text-3xl font-extrabold text-gray-900">تسجيل الدخول
            </h2>
        </div>

        <div class="mt-8 bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <form class="space-y-6" @submit.prevent="handleLogin">
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">
                        البريد الالكتروني
                    </label>
                    <div class="mt-1 relative rounded-md shadow-sm">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i data-feather="mail" class="h-5 w-5 text-gray-400"></i>
                        </div>
                        <input id="email" name="email" type="text" autocomplete="email" required v-model="email"
                            class="py-2 pl-10 block w-full focus:ring-blue-500 focus:border-blue-500 border-gray-300 rounded-md"
                            placeholder="البريد الالكتروني">
                    </div>
                </div>

                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700">
                        كلمة المرور
                    </label>
                    <div class="mt-1 relative rounded-md shadow-sm">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i data-feather="lock" class="h-5 w-5 text-gray-400"></i>
                        </div>
                        <input id="password" name="password" type="password" autocomplete="current-password" required
                            v-model="password"
                            class="py-2 pl-10 block w-full focus:ring-blue-500 focus:border-blue-500 border-gray-300 rounded-md"
                            placeholder="كلمة المرور">
                    </div>
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <input id="remember-me" name="remember-me" type="checkbox" v-model="rememberMe"
                            class="mx-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
                        <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                            تذكرني
                        </label>
                    </div>

                    <div class="text-sm">
                        <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
                            هل نسيت كلمة المرور؟
                        </a>
                    </div>
                </div>

                <div>
                    <button type="submit" :disabled="loading"
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
                        :class="{ 'opacity-50 cursor-not-allowed': loading }">
                        <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                            <i data-feather="log-in" class="h-5 w-5 text-blue-500 group-hover:text-blue-400"></i>
                        </span>
                        {{ loading ? 'تسجيل الدخول...' : 'تسجيل الدخول' }}
                    </button>
                </div>
            </form>

            <div v-if="errorMessage" class="mt-4 p-3 bg-red-100 text-red-700 rounded-md text-sm">
                {{ errorMessage }}
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import feather from 'feather-icons'
import { FrappeApp } from 'frappe-js-sdk'
import { useRouter } from 'vue-router'


export default {
    name: 'Login',
    setup() {
        const email = ref('')
        const password = ref('')
        const rememberMe = ref(false)
        const loading = ref(false)
        const errorMessage = ref('')
        const router = useRouter()

        onMounted(() => {
            feather.replace()
        })

        const handleLogin = async () => {
            loading.value = true
            errorMessage.value = ''

            try {
                // Initialize FrappeJS SDK
                const frappe = new FrappeApp(import.meta.env.VITE_FRAPPE_URL)
                const auth = frappe.auth()

                // Attempt login
                await auth.loginWithUsernamePassword({
                    username: email.value,
                    password: password.value
                })
                console.log('Login successful')
                // router.push('/dashboard')
            } catch (error) {
                console.log('Login error:', error)
                errorMessage.value = error.message || 'Login failed. Please check your credentials.'
            } finally {
                loading.value = false
                // Refresh icons after state changes
                setTimeout(() => feather.replace(), 0)
            }
        }

        return {
            email,
            password,
            rememberMe,
            loading,
            errorMessage,
            handleLogin,
            router  
        }
    }
}
</script>