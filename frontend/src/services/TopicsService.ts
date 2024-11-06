import Api from '@/services/Api'

export default{
  topics(url: string) {
    const params = url ? { url } : {};
    return Api().get("article/topics", {params});
  }
}
