#┌─────────────────────────────────
#│ Web Patio v3.4
#│ init.cgi - 2011/07/06
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'WebPatio v3.4';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#│ 3. 添付画像のうち、以下のファイルを再配布しています。
#│  ・牛飼いとアイコンの部屋 (http://www.ushikai.com/)
#│    alarm.gif book.gif fold4.gif glass.gif memo1.gif memo2.gif
#│    pen.gif trash.gif mente.gif
#└─────────────────────────────────
#
# 【ファイル構成例】
#  scripts
#      |    patio.cgi     [705]
#      |    read.cgi      [705]
#      |    regist.cgi    [705]
#      |    admin.cgi     [705]
#      |    registkey.cgi [705]
#      |    init.cgi      [604]
#      |    note.html
#      |
#      +-- lib / jcode.pl     [604]
#                upload.pl    [604]
#                edit_log.pl  [604]
#                find.pl      [604]
#                check.pl     [604]
#                registkey.pl [604]
#  public_html
#      |    .htaccess     [705]
#      |    dispatch.fcgi [705]
#      +-- data / index1.log  [606]
#      |          index2.log  [606]
#      |          memdata.cgi [606]
#      |
#      +-- log  [707] /
#      |
#      +-- ses  [707] /
#      |
#      +-- upl [707] /
#      |
#      +-- img / *.gif

#===========================================================
#  ◎基本設定
#===========================================================

# 外部ファイル
$jcode   = '../scripts/lib/jcode.pl';
$upload  = '../scripts/lib/upload.pl';
$editlog = '../scripts/lib/edit_log.pl';
$findpl  = '../scripts/lib/find.pl';
$checkpl = '../scripts/lib/check.pl';
$regkeypl = '../scripts/lib/registkey.pl';

# 管理パスワード（英数字で8文字以内）
$pass = '0123';

# アクセス制限をする
# 0=no 1=yes
$authkey = 0;

# ログイン有効期間（分）
$authtime = 60;

# 画像アップを許可する（親記事のみ）
# 0=no 1=yes
$image_upl = 0;

# トリップ機能（ハンドル偽造防止）のための変換キー
# →　英数字で2文字
$trip_key = 'ab';

# タイトル
$title = "ウェブ・パティオ(fluxflex版)";

# タイトルの文字色
$t_color = "#000000";

# タイトルサイズ
$t_size = '18px';

# 本文文字サイズ
$b_size = '13px';

# 本文文字フォント
$b_face = '"MS UI Gothic", Osaka, "ＭＳ Ｐゴシック"';

# 掲示板本体CGI【URLパス】
$bbscgi = './patio.cgi';

# 掲示板投稿CGI【URLパス】
$registcgi = './regist.cgi';

# 掲示板閲覧CGI【URLパス】
$readcgi = './read.cgi';

# 掲示板管理CGI【URLパス】
$admincgi = './admin.cgi';

# 留意事項ページ【URLパス】
$notepage = './note.html';

# 現行ログindex【サーバパス】
$nowfile = './data/index1.log';

# 過去ログindex【サーバパス】
$pastfile = './data/index2.log';

# 会員ファイル【サーバパス】
$memfile = './data/memdata.cgi';

# 記録ファイルディレクトリ【サーバパス】
$logdir = './log';

# セッションディレクトリ【サーバパス】
$sesdir = './ses';

# 戻り先【URLパス】
$home = '../index.html';

# 壁紙
$bg = "";

# 背景色
$bc = "#F0F0F0";

# 文字色
$tx = "#000000";

# リンク色
$lk = "#0000FF";
$vl = "#800080";
$al = "#DD0000";

# 画像ディレクトリ【URLパス】
$imgurl = './img';

# アクセス制限（半角スペースで区切る）
# → 拒否するホスト名又はIPアドレスを記述（アスタリスク可）
# → 記述例 $deny = '*.anonymizer.com 211.154.120.*';
$deny = '';

# 記事の更新は method=POST 限定 (0=no 1=yes)
# （セキュリティ対策）
$postonly = 1;

# 連続投稿の禁止時間（秒）
$wait = 60;

# 禁止ワード
# → 投稿時禁止するワードをコンマで区切る
$no_wd = '';

# 日本語チェック（投稿時日本語が含まれていなければ拒否する）
# 0=No  1=Yes
$jp_wd = 0;

# URL個数チェック
# → 投稿コメント中に含まれるURL個数の最大値
$urlnum = 1;

# 名前入力必須 (0=no 1=yes)
$in_name = 1;

# E-Mail入力必須 (0=no 1=yes)
$in_mail = 0;

# 削除キー入力必須 (0=no 1=yes)
$in_pwd = 0;

# 現行ログ最大スレッド数
# → これを超えると過去ログへ移動
$i_max = 100;

# 過去ログ最大スレッド数
# → これを超えると自動削除
$p_max = 300;

# 1スレッド当りの「表示」記事数
$t_max = 10;

# 1スレッド当りの「最大」記事数
# → これを超えると過去ログへ廻ります
# → 残り90%でアラームを表示します
$m_max = 100;

# 現行ログ初期メニューのスレッド表示数
$menu1 = 10;

# 過去ログ初期メニューのスレッド表示数
$menu2 = 20;

# 色指定（順に、濃色、薄色、中間色）
$col1 = "#8080C0";
$col2 = "#FFFFFF";
$col3 = "#DCDCED";

# 繰越ページ数の当該ページの色
$pglog_col = "#DD0000";

# コメント入力文字数（全角換算）
$max_msg = 800;

# スマイルアイコンの使用 (0=no 1=yes)
$smile = 1;

# スマイルアイコンの定義 (スペースで区切る)
# → ただし、この設定箇所は変更しないほうが無難
# → 顔文字に半角カナや2バイト文字は使用厳禁（正規表現上の制約）
$smile1 = 'smile01.gif smile02.gif smile03.gif smile04.gif smile05.gif smile06.gif smile07.gif';
$smile2 = '(^^) (^_^) (+_+) (^o^) (^^;) (^_-) (;_;)';

# メール送信
# 0 : しない
# 1 : スレッド生成時
# 2 : 投稿記事すべて
$mailing = 0;

# メール送信先
$mailto = 'xxx@xxx.xxx';

# sendmailパス
$sendmail = '/usr/lib/sendmail';

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$gethostbyaddr = 0;

# アクセス制限（半角スペースで区切る、アスタリスク可）
#  → 拒否ホスト名を記述（後方一致）【例】*.anonymizer.com
$deny_host = '';
#  → 拒否IPアドレスを記述（前方一致）【例】210.12.345.*
$deny_addr = '';

# １回当りの最大投稿サイズ (bytes)
# → 例 : 102400 = 100KB
$maxdata = 512000;

# 画像ディレクトリ（画像アップを許可するとき）
# → 順に、サーバパス、URLパス
$upldir = './upl';
$uplurl = './upl';

# アップ画像の最大表示の大きさ（単位：ピクセル）
# → これを超える画像は縮小表示します
$img_max_w = 200;	# 横幅
$img_max_h = 200;	# 縦幅

## --- <以下は「投稿キー」機能（スパム対策）を使用する場合の設定です> --- ##
#
# 投稿キーの使用（スパム対策）
# → 0=no 1=yes
$regist_key = 1;

# 投稿キー画像生成ファイル【URLパス】
$registkeycgi = './registkey.cgi';

# 投稿キー暗号用パスワード（英数字で８文字）
$pcp_passwd = 'patio123';

# 投稿キー許容時間（分単位）
#   投稿フォームを表示させてから、実際に送信ボタンが押される
#   までの可能時間を分単位で指定
$pcp_time = 30;

# 投稿キー画像の大きさ（10ポ or 12ポ）
# 10pt → 10
# 12pt → 12
$regkey_pt = 10;

# 投稿キー画像の文字色
# → $textと合わせると違和感がない。目立たせる場合は #dd0000 など。
$moji_col = '#dd0000';

# 投稿キー画像の背景色
# → $bcと合わせると違和感がない
$back_col = '#F0F0F0';

#===========================================================
#  ◎設定完了
#===========================================================

# 画像拡張子
%imgex = (".jpg" => 1, ".gif" => 1, ".png" => 1);

#-------------------------------------------------
#  アクセス制限
#-------------------------------------------------
sub axscheck {
	# 時間取得
	($time, $date) = &get_time;

	# IP&ホスト取得
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}

	# IPチェック
	my $flg;
	foreach ( split(/\s+/, $deny_addr) ) {
		s/\./\\\./g;
		s/\*/\.\*/g;

		if ($addr =~ /^$_/i) { $flg = 1; last; }
	}
	if ($flg) {
		&error("アクセスを許可されていません");

	# ホストチェック
	} elsif ($host) {

		foreach ( split(/\s+/, $deny_host) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;

			if ($host =~ /$_$/i) { $flg = 1; last; }
		}
		if ($flg) {
			&error("アクセスを許可されていません");
		}
	}
	if ($host eq "") { $host = $addr; }

	## --- 会員制限
	if ($authkey) {

		# ログイン
		if ($mode eq "login") {

			# 初期化
			$my_name = "";
			$my_rank = "";

			# 会員ファイルオープン
			my $flg;
			open(IN,"$memfile") || &error("Open Error: $memfile");
			while (<IN>) {
				my ($id,$pw,$rank,$nam) = split(/<>/);

				if ($in{'id'} eq $id) {
					$flg = 1;

					# 照合
					if (&decrypt($in{'pw'},$pw) == 1) {
						$flg = 2;
						$data = "$rank\t$nam";
						$my_name = $nam;
						$my_rank = $rank;
					}
					last;
				}
			}
			close(IN);

			# 照合不可
			if ($flg < 2) { &error("認証できません"); }

			# セッションID発行
			my @char = (0 .. 9, 'a' .. 'z', 'A' .. 'Z');
			my $cookid;
			srand;
			foreach (1 .. 15) {
				$cookid .= $char[int(rand(@char))];
			}

			# セッションID発行
			open(OUT,"+> $sesdir/$cookid.cgi");
			print OUT "$in{'id'}\t$time\t$data";
			close(OUT);

			# セッションクッキー埋め込み
			print "Set-Cookie: patio_member=$cookid;\n";

			# クッキーID＆ログインID
			$my_ckid = $cookid;
			$my_id   = $in{'id'};

		# ログイン中
		} else {

			# クッキー取得
			my $cook = $ENV{'HTTP_COOKIE'};

			# 該当IDを取り出す
			my %cook;
			foreach ( split(/;/, $cook) ) {
				my ($key,$val) = split(/=/);
				$key =~ s/\s//g;

				$cook{$key} = $val;
			}

			# セッションID有効性をチェック
			if ($cook{'patio_member'} !~ /^[a-zA-Z0-9]{15}$/ || !-e "$sesdir/$cook{'patio_member'}.cgi") {
				&enter_disp;
			}

			# セッションファイル読み取り
			open(IN,"$sesdir/$cook{'patio_member'}.cgi");
			my $ses_data = <IN>;
			close(IN);

			my ($id,$tim,$rank,$nam) = split(/\t/, $ses_data);

			# 時間チェック
			if ($time - $tim > $authtime * 60) {

				unlink("$sesdir/$cook{'patio_member'}.cgi");
				print "Set-Cookie: patio_member=;\n";

				my $msg = qq|ログイン有効時間を経過しました。再度ログインしてください。<br>\n|;
				$msg .= qq|<a href="$bbscgi?mode=enter_disp">【再ログイン】</a>\n|;

				&error($msg);
			}

			# 名前＆クッキーID＆ログインID
			$my_name = $nam;
			$my_ckid = $cook{'patio_member'};
			$my_id   = $id;
			$my_rank = $rank;
		}
	}
}

#-------------------------------------------------
#  フォームデコード
#-------------------------------------------------
sub parse_form {
	undef(%in);
	undef(%fname);
	undef(%uplno);
	undef(%ctype);
	$macbin = 0;
	$postflag = 0;

	# 最大容量チェック
	if ($ENV{'CONTENT_LENGTH'} > $maxdata) {
		my $maxd = int( $maxdata / 1024 ) . "KB";
		&error("容量サイズオーバーです : $maxdまで");
	}

	$postflag = 1;

	# 変数初期化
	local($bound,$key,$val);

	# パラメーター取得
	my @params = $q->param;
	foreach $key (@params) {
		$val = $q->param($key);
		if ($key =~ /^upfile(1|2|3)$/) {
			$uplno = $1;
			$uplno{$uplno} = $uplno;

			# filename属性認識（ファイルアップ）
			if ($uplno && /\s+filename="([^";]+)"/i) {
				$fname{$uplno} = $1;
			}

			# Content-Type認識（ファイルアップ）
			if ($uplno && /Content-Type:\s*([^";]+)/i) {
				local($ctype) = $1;
				$ctype =~ s/\r//g;
				$ctype =~ s/\n//g;

				$ctype{$uplno} = $ctype;
			}

			# ファイル保存
			
		}else{
			# エスケープ
			$val =~ s/&/&amp;/g;
			$val =~ s/"/&quot;/g;
			$val =~ s/</&lt;/g;
			$val =~ s/>/&gt;/g;
			$val =~ s/\r\n/<br>/g;
			$val =~ s/\r/<br>/g;
			$val =~ s/\n/<br>/g;
			$in{$key} = $val;
		}
	}

	$mode = $in{'mode'};
	$p = $in{'p'};
	$i_nam = $in{'name'};
	$i_sub = $in{'sub'};
	$i_com = $in{'comment'};
	$headflag = 0;
}

#-------------------------------------------------
#  HTMLヘッダ
#-------------------------------------------------
sub header {
	my ($sub, $js) = @_;

	if ($sub ne '') { $title = $sub; }
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body,td,th { font-size:$b_size;	font-family:$b_face; }
a:hover { color:$al }
.num { font-size:12px; font-family:Verdana,Helvetica,Arial; }
.s1  { font-size:10px; font-family:Verdana,Helvetica,Arial; }
.s2  { font-size:10px; }
-->
</style>
EOM

	# JavaScript
	if ($js eq "js") {
		print "<Script Language=\"JavaScript\">\n<!--\n";
		print "function MyFace(Smile) {\n";
		print "myComment = document.myFORM.comment.value;\n";
		print "document.myFORM.comment.value = myComment + Smile;\n";
		print "}\n//-->\n</script>\n";
	}

	print "<title>$title</title></head>\n";

	# bodyタグ
	if ($bg) {
		print qq|<body background="$bg" bgcolor="$bc" text="$tx" link="$lk" vlink="$vl" alink="$al">\n|;
	} else {
		print qq|<body bgcolor="$bc" text="$tx" link="$lk" vlink="$vl" alink="$al">\n|;
	}
	$headflag = 1;
}

#-------------------------------------------------
#  エラー処理
#-------------------------------------------------
sub error {
	&header if (!$headflag);
	print <<"EOM";
<div align="center">
<h3>ERROR !</h3>
<p><font color="red">$_[0]</font></p>
<form>
<input type="button" value="前画面にもどる" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  時間取得
#-------------------------------------------------
sub get_time {
	$ENV{'TZ'} = "JST-9";
	my $time = time;
	my ($min,$hour,$mday,$mon,$year) = (localtime($time))[1..5];

	# 日時のフォーマット
	my $date = sprintf("%04d/%02d/%02d %02d:%02d", $year+1900,$mon+1,$mday,$hour,$min);
	return ($time, $date);
}

#-------------------------------------------------
#  入室画面
#-------------------------------------------------
sub enter_disp {
	&header;
	print <<EOM;
<div align="center">
<table><tr><td>
・ 入室にはログインIDとパスワードが必要です。<br>
・ ブラウザのクッキーは必ず有効にしてください。
</td></tr></table>
<form action="$bbscgi" method="post">
<input type="hidden" name="mode" value="login">
<Table border="0" cellspacing="0" cellpadding="0" width="200">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col2" nowrap align="center">ログインID</td>
  <td bgcolor="$col2" nowrap><input type="text" name="id" value="" size="20" style="width:160px"></td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" nowrap align="center">パスワード</td>
  <td bgcolor="$col2" nowrap><input type="password" name="pw" value="" size="20" style="width:160px"></td>
</tr>
</table>
</Td></Tr></Table>
<p></p>
<input type="submit" value="ログイン" style="width:80px">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  crypt暗号
#-------------------------------------------------
sub encrypt {
	my ($inpw) = @_;

	# 文字列定義
	my @char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');

	# 乱数で種を生成
	srand;
	my $salt = $char[int(rand(@char))] . $char[int(rand(@char))];

	# 暗号化
	crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
}

#-------------------------------------------------
#  crypt照合
#-------------------------------------------------
sub decrypt {
	my ($inpw, $enpw) = @_;

	if ($enpw eq "") { &error("認証できません"); }

	# 種抜き出し
	my $salt = $enpw =~ /^\$1\$(.*)\$/ && $1 || substr($enpw, 0, 2);

	# 照合処理
	if (crypt($inpw, $salt) eq $enpw || crypt($inpw, '$1$' . $salt) eq $enpw) {
		return 1;
	} else {
		return 0;
	}
}



1;

