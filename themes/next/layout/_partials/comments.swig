{% if page.comments %}
  <div class="comments" id="comments">
    {% if (theme.duoshuo and theme.duoshuo.shortname) or theme.duoshuo_shortname %}
      <div class="ds-thread" data-thread-key="{{ page.path }}"
           data-title="{{ page.title }}" data-url="{{ page.permalink }}">
      </div>
      <div class="ds-share" data-thread-key="{{page.path}}" data-title="{{page.title}}" data-images="images/qiu.jpg" data-content="我想说：" data-url="{{page.permalink}}">
      <div class="ds-share-inline">
      <ul  class="ds-share-icons-16">

    <li data-toggle="ds-share-icons-more"><a class="ds-more" href="javascript:void(0);">分享到：</a></li>
    <li><a class="ds-weibo" href="javascript:void(0);" data-service="weibo">微博</a></li>
    <li><a class="ds-qzone" href="javascript:void(0);" data-service="qzone">QQ空间</a></li>
    <li><a class="ds-wechat" href="javascript:void(0);" data-service="wechat">微信</a></li>

  </ul>
  <div class="ds-share-icons-more">
  </div>
</div>
</div>
    {% elseif theme.facebook_sdk.enable and theme.facebook_comments_plugin.enable %}
      <div class="fb-comments"
           data-href="{{ page.permalink }}"
           data-numposts="{{ theme.facebook_comments_plugin.num_of_posts }}"
           data-width="{{ theme.facebook_comments_plugin.width }}"
           data-colorscheme="{{ theme.facebook_comments_plugin.scheme }}">
      </div>
    {% elseif theme.disqus_shortname %}
      <div id="disqus_thread">
        <noscript>
          Please enable JavaScript to view the
          <a href="//disqus.com/?ref_noscript">comments powered by Disqus.</a>
        </noscript>
      </div>
    {% elseif theme.hypercomments_id %}
      <div id="hypercomments_widget"></div>
    {% elseif theme.gentie_productKey %}
      <div id="cloud-tie-wrapper" class="cloud-tie-wrapper"></div>
    {% elseif theme.youyan_uid %}
      <div id="uyan_frame"></div>
    {% endif %}
  </div>
{% endif %}
