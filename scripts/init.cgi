#��������������������������������������������������������������������
#�� Web Patio v3.4
#�� init.cgi - 2011/07/06
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'WebPatio v3.4';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#�� 3. �Y�t�摜�̂����A�ȉ��̃t�@�C�����Ĕz�z���Ă��܂��B
#��  �E�������ƃA�C�R���̕��� (http://www.ushikai.com/)
#��    alarm.gif book.gif fold4.gif glass.gif memo1.gif memo2.gif
#��    pen.gif trash.gif mente.gif
#��������������������������������������������������������������������
#
# �y�t�@�C���\����z
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
#  ����{�ݒ�
#===========================================================

# �O���t�@�C��
$jcode   = '../scripts/lib/jcode.pl';
$upload  = '../scripts/lib/upload.pl';
$editlog = '../scripts/lib/edit_log.pl';
$findpl  = '../scripts/lib/find.pl';
$checkpl = '../scripts/lib/check.pl';
$regkeypl = '../scripts/lib/registkey.pl';

# �Ǘ��p�X���[�h�i�p������8�����ȓ��j
$pass = '0123';

# �A�N�Z�X����������
# 0=no 1=yes
$authkey = 0;

# ���O�C���L�����ԁi���j
$authtime = 60;

# �摜�A�b�v��������i�e�L���̂݁j
# 0=no 1=yes
$image_upl = 0;

# �g���b�v�@�\�i�n���h���U���h�~�j�̂��߂̕ϊ��L�[
# ���@�p������2����
$trip_key = 'ab';

# �^�C�g��
$title = "�E�F�u�E�p�e�B�I(fluxflex��)";

# �^�C�g���̕����F
$t_color = "#000000";

# �^�C�g���T�C�Y
$t_size = '18px';

# �{�������T�C�Y
$b_size = '13px';

# �{�������t�H���g
$b_face = '"MS UI Gothic", Osaka, "�l�r �o�S�V�b�N"';

# �f���{��CGI�yURL�p�X�z
$bbscgi = './patio.cgi';

# �f�����eCGI�yURL�p�X�z
$registcgi = './regist.cgi';

# �f���{��CGI�yURL�p�X�z
$readcgi = './read.cgi';

# �f���Ǘ�CGI�yURL�p�X�z
$admincgi = './admin.cgi';

# ���ӎ����y�[�W�yURL�p�X�z
$notepage = './note.html';

# ���s���Oindex�y�T�[�o�p�X�z
$nowfile = './data/index1.log';

# �ߋ����Oindex�y�T�[�o�p�X�z
$pastfile = './data/index2.log';

# ����t�@�C���y�T�[�o�p�X�z
$memfile = './data/memdata.cgi';

# �L�^�t�@�C���f�B���N�g���y�T�[�o�p�X�z
$logdir = './log';

# �Z�b�V�����f�B���N�g���y�T�[�o�p�X�z
$sesdir = './ses';

# �߂��yURL�p�X�z
$home = '../index.html';

# �ǎ�
$bg = "";

# �w�i�F
$bc = "#F0F0F0";

# �����F
$tx = "#000000";

# �����N�F
$lk = "#0000FF";
$vl = "#800080";
$al = "#DD0000";

# �摜�f�B���N�g���yURL�p�X�z
$imgurl = './img';

# �A�N�Z�X�����i���p�X�y�[�X�ŋ�؂�j
# �� ���ۂ���z�X�g������IP�A�h���X���L�q�i�A�X�^���X�N�j
# �� �L�q�� $deny = '*.anonymizer.com 211.154.120.*';
$deny = '';

# �L���̍X�V�� method=POST ���� (0=no 1=yes)
# �i�Z�L�����e�B�΍�j
$postonly = 1;

# �A�����e�̋֎~���ԁi�b�j
$wait = 60;

# �֎~���[�h
# �� ���e���֎~���郏�[�h���R���}�ŋ�؂�
$no_wd = '';

# ���{��`�F�b�N�i���e�����{�ꂪ�܂܂�Ă��Ȃ���΋��ۂ���j
# 0=No  1=Yes
$jp_wd = 0;

# URL���`�F�b�N
# �� ���e�R�����g���Ɋ܂܂��URL���̍ő�l
$urlnum = 1;

# ���O���͕K�{ (0=no 1=yes)
$in_name = 1;

# E-Mail���͕K�{ (0=no 1=yes)
$in_mail = 0;

# �폜�L�[���͕K�{ (0=no 1=yes)
$in_pwd = 0;

# ���s���O�ő�X���b�h��
# �� ����𒴂���Ɖߋ����O�ֈړ�
$i_max = 100;

# �ߋ����O�ő�X���b�h��
# �� ����𒴂���Ǝ����폜
$p_max = 300;

# 1�X���b�h����́u�\���v�L����
$t_max = 10;

# 1�X���b�h����́u�ő�v�L����
# �� ����𒴂���Ɖߋ����O�։��܂�
# �� �c��90%�ŃA���[����\�����܂�
$m_max = 100;

# ���s���O�������j���[�̃X���b�h�\����
$menu1 = 10;

# �ߋ����O�������j���[�̃X���b�h�\����
$menu2 = 20;

# �F�w��i���ɁA�Z�F�A���F�A���ԐF�j
$col1 = "#8080C0";
$col2 = "#FFFFFF";
$col3 = "#DCDCED";

# �J�z�y�[�W���̓��Y�y�[�W�̐F
$pglog_col = "#DD0000";

# �R�����g���͕������i�S�p���Z�j
$max_msg = 800;

# �X�}�C���A�C�R���̎g�p (0=no 1=yes)
$smile = 1;

# �X�}�C���A�C�R���̒�` (�X�y�[�X�ŋ�؂�)
# �� �������A���̐ݒ�ӏ��͕ύX���Ȃ��ق�������
# �� �當���ɔ��p�J�i��2�o�C�g�����͎g�p���ցi���K�\����̐���j
$smile1 = 'smile01.gif smile02.gif smile03.gif smile04.gif smile05.gif smile06.gif smile07.gif';
$smile2 = '(^^) (^_^) (+_+) (^o^) (^^;) (^_-) (;_;)';

# ���[�����M
# 0 : ���Ȃ�
# 1 : �X���b�h������
# 2 : ���e�L�����ׂ�
$mailing = 0;

# ���[�����M��
$mailto = 'xxx@xxx.xxx';

# sendmail�p�X
$sendmail = '/usr/lib/sendmail';

# �z�X�g�擾���@
# 0 : gethostbyaddr�֐����g��Ȃ�
# 1 : gethostbyaddr�֐����g��
$gethostbyaddr = 0;

# �A�N�Z�X�����i���p�X�y�[�X�ŋ�؂�A�A�X�^���X�N�j
#  �� ���ۃz�X�g�����L�q�i�����v�j�y��z*.anonymizer.com
$deny_host = '';
#  �� ����IP�A�h���X���L�q�i�O����v�j�y��z210.12.345.*
$deny_addr = '';

# �P�񓖂�̍ő哊�e�T�C�Y (bytes)
# �� �� : 102400 = 100KB
$maxdata = 512000;

# �摜�f�B���N�g���i�摜�A�b�v��������Ƃ��j
# �� ���ɁA�T�[�o�p�X�AURL�p�X
$upldir = './upl';
$uplurl = './upl';

# �A�b�v�摜�̍ő�\���̑傫���i�P�ʁF�s�N�Z���j
# �� ����𒴂���摜�͏k���\�����܂�
$img_max_w = 200;	# ����
$img_max_h = 200;	# �c��

## --- <�ȉ��́u���e�L�[�v�@�\�i�X�p���΍�j���g�p����ꍇ�̐ݒ�ł�> --- ##
#
# ���e�L�[�̎g�p�i�X�p���΍�j
# �� 0=no 1=yes
$regist_key = 1;

# ���e�L�[�摜�����t�@�C���yURL�p�X�z
$registkeycgi = './registkey.cgi';

# ���e�L�[�Í��p�p�X���[�h�i�p�����łW�����j
$pcp_passwd = 'patio123';

# ���e�L�[���e���ԁi���P�ʁj
#   ���e�t�H�[����\�������Ă���A���ۂɑ��M�{�^�����������
#   �܂ł̉\���Ԃ𕪒P�ʂŎw��
$pcp_time = 30;

# ���e�L�[�摜�̑傫���i10�| or 12�|�j
# 10pt �� 10
# 12pt �� 12
$regkey_pt = 10;

# ���e�L�[�摜�̕����F
# �� $text�ƍ��킹��ƈ�a�����Ȃ��B�ڗ�������ꍇ�� #dd0000 �ȂǁB
$moji_col = '#dd0000';

# ���e�L�[�摜�̔w�i�F
# �� $bc�ƍ��킹��ƈ�a�����Ȃ�
$back_col = '#F0F0F0';

#===========================================================
#  ���ݒ芮��
#===========================================================

# �摜�g���q
%imgex = (".jpg" => 1, ".gif" => 1, ".png" => 1);

#-------------------------------------------------
#  �A�N�Z�X����
#-------------------------------------------------
sub axscheck {
	# ���Ԏ擾
	($time, $date) = &get_time;

	# IP&�z�X�g�擾
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}

	# IP�`�F�b�N
	my $flg;
	foreach ( split(/\s+/, $deny_addr) ) {
		s/\./\\\./g;
		s/\*/\.\*/g;

		if ($addr =~ /^$_/i) { $flg = 1; last; }
	}
	if ($flg) {
		&error("�A�N�Z�X��������Ă��܂���");

	# �z�X�g�`�F�b�N
	} elsif ($host) {

		foreach ( split(/\s+/, $deny_host) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;

			if ($host =~ /$_$/i) { $flg = 1; last; }
		}
		if ($flg) {
			&error("�A�N�Z�X��������Ă��܂���");
		}
	}
	if ($host eq "") { $host = $addr; }

	## --- �������
	if ($authkey) {

		# ���O�C��
		if ($mode eq "login") {

			# ������
			$my_name = "";
			$my_rank = "";

			# ����t�@�C���I�[�v��
			my $flg;
			open(IN,"$memfile") || &error("Open Error: $memfile");
			while (<IN>) {
				my ($id,$pw,$rank,$nam) = split(/<>/);

				if ($in{'id'} eq $id) {
					$flg = 1;

					# �ƍ�
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

			# �ƍ��s��
			if ($flg < 2) { &error("�F�؂ł��܂���"); }

			# �Z�b�V����ID���s
			my @char = (0 .. 9, 'a' .. 'z', 'A' .. 'Z');
			my $cookid;
			srand;
			foreach (1 .. 15) {
				$cookid .= $char[int(rand(@char))];
			}

			# �Z�b�V����ID���s
			open(OUT,"+> $sesdir/$cookid.cgi");
			print OUT "$in{'id'}\t$time\t$data";
			close(OUT);

			# �Z�b�V�����N�b�L�[���ߍ���
			print "Set-Cookie: patio_member=$cookid;\n";

			# �N�b�L�[ID�����O�C��ID
			$my_ckid = $cookid;
			$my_id   = $in{'id'};

		# ���O�C����
		} else {

			# �N�b�L�[�擾
			my $cook = $ENV{'HTTP_COOKIE'};

			# �Y��ID�����o��
			my %cook;
			foreach ( split(/;/, $cook) ) {
				my ($key,$val) = split(/=/);
				$key =~ s/\s//g;

				$cook{$key} = $val;
			}

			# �Z�b�V����ID�L�������`�F�b�N
			if ($cook{'patio_member'} !~ /^[a-zA-Z0-9]{15}$/ || !-e "$sesdir/$cook{'patio_member'}.cgi") {
				&enter_disp;
			}

			# �Z�b�V�����t�@�C���ǂݎ��
			open(IN,"$sesdir/$cook{'patio_member'}.cgi");
			my $ses_data = <IN>;
			close(IN);

			my ($id,$tim,$rank,$nam) = split(/\t/, $ses_data);

			# ���ԃ`�F�b�N
			if ($time - $tim > $authtime * 60) {

				unlink("$sesdir/$cook{'patio_member'}.cgi");
				print "Set-Cookie: patio_member=;\n";

				my $msg = qq|���O�C���L�����Ԃ��o�߂��܂����B�ēx���O�C�����Ă��������B<br>\n|;
				$msg .= qq|<a href="$bbscgi?mode=enter_disp">�y�ă��O�C���z</a>\n|;

				&error($msg);
			}

			# ���O���N�b�L�[ID�����O�C��ID
			$my_name = $nam;
			$my_ckid = $cook{'patio_member'};
			$my_id   = $id;
			$my_rank = $rank;
		}
	}
}

#-------------------------------------------------
#  �t�H�[���f�R�[�h
#-------------------------------------------------
sub parse_form {
	undef(%in);
	undef(%fname);
	undef(%uplno);
	undef(%ctype);
	$macbin = 0;
	$postflag = 0;

	# �ő�e�ʃ`�F�b�N
	if ($ENV{'CONTENT_LENGTH'} > $maxdata) {
		my $maxd = int( $maxdata / 1024 ) . "KB";
		&error("�e�ʃT�C�Y�I�[�o�[�ł� : $maxd�܂�");
	}

	$postflag = 1;

	# �ϐ�������
	local($bound,$key,$val);

	# �p�����[�^�[�擾
	my @params = $q->param;
	foreach $key (@params) {
		$val = $q->param($key);
		if ($key =~ /^upfile(1|2|3)$/) {
			$uplno = $1;
			$uplno{$uplno} = $uplno;

			# filename�����F���i�t�@�C���A�b�v�j
			if ($uplno && /\s+filename="([^";]+)"/i) {
				$fname{$uplno} = $1;
			}

			# Content-Type�F���i�t�@�C���A�b�v�j
			if ($uplno && /Content-Type:\s*([^";]+)/i) {
				local($ctype) = $1;
				$ctype =~ s/\r//g;
				$ctype =~ s/\n//g;

				$ctype{$uplno} = $ctype;
			}
		}else{
			# �G�X�P�[�v
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
#  HTML�w�b�_
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

	# body�^�O
	if ($bg) {
		print qq|<body background="$bg" bgcolor="$bc" text="$tx" link="$lk" vlink="$vl" alink="$al">\n|;
	} else {
		print qq|<body bgcolor="$bc" text="$tx" link="$lk" vlink="$vl" alink="$al">\n|;
	}
	$headflag = 1;
}

#-------------------------------------------------
#  �G���[����
#-------------------------------------------------
sub error {
	&header if (!$headflag);
	print <<"EOM";
<div align="center">
<h3>ERROR !</h3>
<p><font color="red">$_[0]</font></p>
<form>
<input type="button" value="�O��ʂɂ��ǂ�" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���Ԏ擾
#-------------------------------------------------
sub get_time {
	$ENV{'TZ'} = "JST-9";
	my $time = time;
	my ($min,$hour,$mday,$mon,$year) = (localtime($time))[1..5];

	# �����̃t�H�[�}�b�g
	my $date = sprintf("%04d/%02d/%02d %02d:%02d", $year+1900,$mon+1,$mday,$hour,$min);
	return ($time, $date);
}

#-------------------------------------------------
#  �������
#-------------------------------------------------
sub enter_disp {
	&header;
	print <<EOM;
<div align="center">
<table><tr><td>
�E �����ɂ̓��O�C��ID�ƃp�X���[�h���K�v�ł��B<br>
�E �u���E�U�̃N�b�L�[�͕K���L���ɂ��Ă��������B
</td></tr></table>
<form action="$bbscgi" method="post">
<input type="hidden" name="mode" value="login">
<Table border="0" cellspacing="0" cellpadding="0" width="200">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col2">
  <td bgcolor="$col2" nowrap align="center">���O�C��ID</td>
  <td bgcolor="$col2" nowrap><input type="text" name="id" value="" size="20" style="width:160px"></td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" nowrap align="center">�p�X���[�h</td>
  <td bgcolor="$col2" nowrap><input type="password" name="pw" value="" size="20" style="width:160px"></td>
</tr>
</table>
</Td></Tr></Table>
<p></p>
<input type="submit" value="���O�C��" style="width:80px">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  crypt�Í�
#-------------------------------------------------
sub encrypt {
	my ($inpw) = @_;

	# �������`
	my @char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');

	# �����Ŏ�𐶐�
	srand;
	my $salt = $char[int(rand(@char))] . $char[int(rand(@char))];

	# �Í���
	crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
}

#-------------------------------------------------
#  crypt�ƍ�
#-------------------------------------------------
sub decrypt {
	my ($inpw, $enpw) = @_;

	if ($enpw eq "") { &error("�F�؂ł��܂���"); }

	# �픲���o��
	my $salt = $enpw =~ /^\$1\$(.*)\$/ && $1 || substr($enpw, 0, 2);

	# �ƍ�����
	if (crypt($inpw, $salt) eq $enpw || crypt($inpw, '$1$' . $salt) eq $enpw) {
		return 1;
	} else {
		return 0;
	}
}



1;

