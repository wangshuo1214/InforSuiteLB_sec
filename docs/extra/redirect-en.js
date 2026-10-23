(function(){
  try {
    var path = window.location.pathname || '';
    // Normalize multiple slashes
    path = path.replace(/\/+/g, '/');

    // Slug conversion map (old underscore/camelCase to new dash format)
    var slugMap = {
      'add_header_content_type': 'add-header-content-type',
      'addheadermultiline': 'add-header-multiline',
      'addheaderredefinition': 'add-header-redefinition',
      'aliastraversal': 'alias-traversal',
      'allow_without_deny': 'allow-without-deny',
      'default_server_flag': 'default-server-flag',
      'error_log_off': 'error-log-off',
      'hash_without_default': 'hash-without-default',
      'hostspoofing': 'host-spoofing',
      'hsts_header': 'hsts-header',
      'http2_misdirected_request': 'http2-misdirected-request',
      'httpsplitting': 'http-splitting',
      'if_is_evil': 'if-is-evil',
      'invalid_regex': 'invalid-regex',
      'low_keepalive_requests': 'low-keepalive-requests',
      'missing_resolver': 'missing-resolver',
      'proxy_pass_normalized': 'proxy-pass-normalized',
      'regex_redos': 'regex-redos',
      'resolver_external': 'resolver-external',
      'return_bypasses_allow_deny': 'return-bypasses-allow-deny',
      'try_files_is_evil_too': 'try-files-is-evil-too',
      'unanchored_regex': 'unanchored-regex',
      'validreferers': 'valid-referers',
      'version_disclosure': 'version-disclosure',
      'weak_ssl_tls': 'weak-ssl-tls',
      'worker_rlimit_nofile_vs_connections': 'worker-rlimit-nofile-vs-connections'
    };

    // If path starts with /en/, redirect to path without /en/
    if (path.indexOf('/en/') === 0) {
      var newPath = path.replace(/^\/en\//, '/');
      var newUrl = newPath + window.location.search + window.location.hash;
      window.location.replace(newUrl);
      return;
    }

    // Redirect /plugins/* to /checks/* (preserving locale prefix if present)
    var pluginsMatch = path.match(/^(\/(?:ru|zh)?)?\/plugins\/([^\/]+)\/?$/);
    if (pluginsMatch) {
      var localePrefix = pluginsMatch[1] || '';
      var oldSlug = pluginsMatch[2];
      var newSlug = slugMap[oldSlug] || oldSlug;
      var newUrl = localePrefix + '/checks/' + newSlug + '/' + window.location.search + window.location.hash;
      window.location.replace(newUrl);
      return;
    }

    // Redirect old check slugs to new dash format
    var checksMatch = path.match(/^(\/(?:ru|zh)?)?\/checks\/([^\/]+)\/?$/);
    if (checksMatch) {
      var localePrefix = checksMatch[1] || '';
      var oldSlug = checksMatch[2];
      if (slugMap[oldSlug]) {
        var newUrl = localePrefix + '/checks/' + slugMap[oldSlug] + '/' + window.location.search + window.location.hash;
        window.location.replace(newUrl);
        return;
      }
    }
  } catch (e) {
    // no-op
  }
})();
