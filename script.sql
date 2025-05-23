drop table cam_oco_captura cascade constraints;
drop table usu_oco_participa cascade constraints;
drop table func_ocorr_atende cascade constraints;
drop table ocorrencia cascade constraints;
drop table cco cascade constraints;
drop table estaca_linha_possui cascade constraints;
drop table linha cascade constraints;
drop table estacao cascade constraints;
drop table camera cascade constraints;
drop table vagao_carro cascade constraints;
drop table trem cascade constraints;
drop table tercerizado cascade constraints;
drop table efetivo cascade constraints;
drop table funcionario cascade constraints;
drop table cargo cascade constraints;
drop table usuario cascade constraints;
drop table evidencia cascade constraints;


create table cargo (
   id_cargo     number
      generated by default on null as identity
      constraint cargo_id_pk primary key,
   nome_cargo   varchar2(50)
      constraint cargo_nome_uk unique,
   salario_base number(7,2)
);


create table funcionario (
   id_funcionario    number
      generated by default on null as identity
      constraint func_id_pk primary key,
   nome              varchar2(50)
      constraint func_nome_nn not null,
   status            number(1)
      constraint func_status_nn not null,
   sexo_funcionario  char(1),
   fk_cargo_id_cargo number
      constraint func_cargo_fk
         references cargo ( id_cargo )
);


create table efetivo (
   fk_funcionario_id_funcionario number
      constraint efetivo_func_fk
         references funcionario ( id_funcionario ),
   ctps                          char(15)
      constraint ctps_uk unique,
   cpf_efetivo                   char(11),
   data_registro                 date
      constraint efetivo_dr_nn not null,
   constraint efetivo_id_pk primary key ( fk_funcionario_id_funcionario )
);


create table tercerizado (
   fk_funcionario_id_funcionario number
      constraint terce_func_fk
         references funcionario ( id_funcionario ),
   nome_social                   varchar2(50),
   cnpj_associado                char(14),
   constraint terce_id_pk primary key ( fk_funcionario_id_funcionario )
);


create table trem (
   nmr_trem       number
      generated by default on null as identity
      constraint trem_id_pk primary key,
   fabricante     varchar2(10),
   data_fabr_trem date
      constraint trem_data_nn not null,
   modelo_trem    varchar2(10)
);


create table vagao_carro (
   id_carro         number
      generated by default on null as identity
      constraint vagao_id_pk primary key,
   data_fabr_vagao  date
      constraint vagao_data_nn not null,
   modelo_vagao     varchar2(10),
   fabricante_vagao varchar2(50),
   fk_trem_nmr_trem number
      constraint vagao_trem_fk
         references trem ( nmr_trem )
);

create table camera (
   id_camera               number
      generated by default on null as identity
      constraint cam_id_pk primary key,
   modelo_camera           varchar2(10),
   resolucao_camera        char(2),
   posicao_no_vagao        char(2),
   fk_vagao_carro_id_carro number
      constraint cam_vagao_fk
         references vagao_carro ( id_carro )
);


create table estacao (
   id_estacao     number
      generated by default on null as identity
      constraint est_id_pk primary key,
   nome_estacao   varchar2(30),
   nr_plataformas number(2)
);

create table linha (
   nome_linha      varchar2(25)
      constraint linha_id_pk primary key,
   extencao        number(4,2),
   regioes_pertenc varchar2(30)
);

create table estaca_linha_possui (
   fk_linha_nome_linha   varchar2(25)
      constraint elp_linha_fk
         references linha ( nome_linha ),
   fk_estacao_id_estacao number
      constraint elp_estacao_fk
         references estacao ( id_estacao ),
   constraint elp_pk primary key ( fk_linha_nome_linha,
                                   fk_estacao_id_estacao )
);

create table cco (
   id_cco       number
      generated by default on null as identity
      constraint cco_id_pk primary key,
   endereco_cco varchar2(60),
   telefone     char(9)
);

create table ocorrencia (
   id_ocorrencia         number
      generated by default on null as identity
      constraint oc_id_pk primary key,
   data_inicio           date
      constraint oc_datai_nn not null,
   data_fim              date,
   tipo_ocorrencia       varchar2(36),
   descricao_ocorrencia  varchar(500),
   severidade_ocorrencia number(1)
      constraint oc_sever_nn not null,
   fk_cco_id_cco         number
      constraint oc_cco_fk
         references cco ( id_cco ),
   fk_estacao_id_estacao number
      constraint oc_estacao_fk
         references estacao ( id_estacao ),
   status_ocorrencia     varchar2(20) default 'ABERTO' not null
);


create table func_ocorr_atende (
   data_inicio_atendimento       date
      constraint foa_datai_nn not null,
   fk_funcionario_id_funcionario number
      constraint foa_func_fk
         references funcionario ( id_funcionario ),
   fk_ocorrencia_id_ocorrencia   number
      constraint foa_ocorr_fk
         references ocorrencia ( id_ocorrencia ),
   constraint foa_pk primary key ( fk_funcionario_id_funcionario,
                                   fk_ocorrencia_id_ocorrencia )
);

create table usuario (
   cpf_usuario       char(11)
      constraint usu_id_pk primary key,
   idade_usuario     number(3),
   descricao_usuario varchar2(60),
   sexo_usuario      char(1),
   nome_usuario      varchar2(50)
);


create table usu_oco_participa (
   fk_usuario_cpf_usuario      char(11)
      constraint uopar_usu_fk
         references usuario ( cpf_usuario ),
   fk_ocorrencia_id_ocorrencia number
      constraint uopar_ocorr_fk
         references ocorrencia ( id_ocorrencia ),
   constraint uop_pk primary key ( fk_usuario_cpf_usuario,
                                   fk_ocorrencia_id_ocorrencia )
);


create table cam_oco_captura (
   data_captura                date
      constraint camoco_data_nn not null,
   fk_camera_id_camera         number
      constraint cameroco_cam_fk
         references camera ( id_camera ),
   fk_ocorrencia_id_ocorrencia number
      constraint cameroco_ocorr_fk
         references ocorrencia ( id_ocorrencia ),
   constraint camoco_pk primary key ( fk_camera_id_camera,
                                      fk_ocorrencia_id_ocorrencia )
);

create table evidencia (
   id            number
      generated by default on null as identity
      constraint ev_id_pk primary key,
   id_ocorrencia number
      constraint fk_evid_ocorr
         references ocorrencia ( id_ocorrencia ),
   s3_key        varchar2(512) not null,
   descricao     varchar2(200),
   data_upload   timestamp default systimestamp
);


insert into estacao (
   nome_estacao,
   nr_plataformas
) values ( 'Estação Central',
           5 );

insert into cco (
   id_cco,
   endereco_cco,
   telefone
) values ( 1,
           'Rua Exemplo, 123',
           '123456789' );
commit;

delete from ocorrencia;


alter table ocorrencia add status_ocorrencia varchar(20) default 'ABERTO' not null



-- Inserir duas estações de exemplo
INSERT INTO estacao (nome_estacao, nr_plataformas) VALUES ('Estação Novo Horizonte', 3), ('Estação Vila Boa', 2);


select * from estacao;