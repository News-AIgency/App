import Api from '@/services/Api'

export default {
    article(url: string, selected_topic: string) {
        return Api().post("article/generate", {
            "url": url,
            "selected_topic": selected_topic
        })
    }
}
