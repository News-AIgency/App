import Api from '@/services/Api'

export default {
  topics(url: string) {
    return Api().post("article/topics", {
      "url": url
    });
  }
}
