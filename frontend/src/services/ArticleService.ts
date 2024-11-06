import Api from '@/services/Api'

export default {
    article(url: string, selected_topic: string) {
        return Api().get("article/generate", {
            params: {
                "url": url,
                "selected_topic": selected_topic
            }
        })
    }
}
