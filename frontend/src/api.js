import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

export async function health() {
  return axios.get('/health')
}

export async function generate(payload) {
  return api.post('/generate', payload)
}

export async function listConversations(params) {
  return api.get('/conversations', { params })
}

export async function getConversation(id) {
  return api.get(`/conversations/${id}`)
}

export async function deleteConversation(id) {
  return api.delete(`/conversations/${id}`)
}

export async function getStats() {
  return api.get('/stats')
}

export default api
