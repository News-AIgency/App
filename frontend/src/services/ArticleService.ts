import Api from '@/services/Api'

export default {
  article(url: string, selected_topic: string, storm: boolean) {
    return Api().post('article/generate', {
      url: url,
      selected_topic: selected_topic,
      storm: storm,
    })
  },
  regenerateEngagingText(
    url?: string,
    id?: number,
    selected_topic?: string,
    old_engaging_text?: string,
    current_headline?: string,
  ) {
    return Api().post('regenerate/engaging_text', {
      url: url,
      id: id,
      selected_topic: selected_topic,
      old_engaging_text: old_engaging_text,
      current_headline: current_headline,
    })
  },
  regeneratePerex(
    url?: string,
    id?: number,
    selected_topic?: string,
    old_perex?: string,
    current_headline?: string,
  ) {
    return Api().post('regenerate/perex', {
      url: url,
      id: id,
      selected_topic: selected_topic,
      old_perex: old_perex,
      current_headline: current_headline,
    })
  },
  regenerateBody(
    url?: string,
    id?: number,
    selected_topic?: string,
    old_article_body?: string,
    current_headline?: string,
  ) {
    return Api().post('regenerate/articlebody', {
      url: url,
      id: id,
      selected_topic: selected_topic,
      old_article_body: old_article_body,
      current_headline: current_headline,
    })
  },
  regenerateSuggestions(
    url?: string,
    id?: number,
    selected_topic?: string,
    old_headlines?: string[],
  ) {
    return Api().post('regenerate/headlines', {
      url: url,
      id: id,
      selected_topic: selected_topic,
      old_headlines: old_headlines,
    })
  },

}
