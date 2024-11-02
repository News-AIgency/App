import Api from '@/services/Api'

export default{
  topics() {
    return Api().get("article/topics")
  }
}
